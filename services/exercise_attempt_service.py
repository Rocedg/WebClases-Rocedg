from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import ast
import json
import math
import re
import unicodedata

from database import db
from models import ExerciseAttempt, ExerciseResponse, utc_now
from services.activity_service import mark_exercise_worked, record_activity_event


ATTEMPT_STARTED = "started"
ATTEMPT_SUBMITTED = "submitted"
ATTEMPT_REVIEWED = "reviewed"

GRADE_UNGRADED = "ungraded"
GRADE_CORRECT = "correct"
GRADE_INCORRECT = "incorrect"
GRADE_PENDING_REVIEW = "pending_review"

OPEN_RESPONSE_TYPES = {
    "short_text",
    "written_upload",
    "open_text",
    "text",
    "textarea",
    "numeric_or_expression_placeholder",
}

NUMERIC_RE = re.compile(r"^[+-]?\d+(?:[\.,]\d+)?(?:[eE][+-]?\d+)?$")
FRACTION_RE = re.compile(r"^([+-]?\d+(?:[\.,]\d+)?)\/([+-]?\d+(?:[\.,]\d+)?)$")
UNIT_TOKEN_RE = re.compile(r"[A-Za-zΩ]+|[*/()^]|\d+|[-+]")

UNIT_DEFINITIONS = {
    "kg": (Decimal("1"), {"kg": 1}),
    "g": (Decimal("0.001"), {"kg": 1}),
    "m": (Decimal("1"), {"m": 1}),
    "cm": (Decimal("0.01"), {"m": 1}),
    "mm": (Decimal("0.001"), {"m": 1}),
    "km": (Decimal("1000"), {"m": 1}),
    "s": (Decimal("1"), {"s": 1}),
    "min": (Decimal("60"), {"s": 1}),
    "h": (Decimal("3600"), {"s": 1}),
    "A": (Decimal("1"), {"A": 1}),
    "K": (Decimal("1"), {"K": 1}),
    "mol": (Decimal("1"), {"mol": 1}),
    "rad": (Decimal("1"), {"rad": 1}),
    "C": (Decimal("1"), {"A": 1, "s": 1}),
    "N": (Decimal("1"), {"kg": 1, "m": 1, "s": -2}),
    "J": (Decimal("1"), {"kg": 1, "m": 2, "s": -2}),
    "W": (Decimal("1"), {"kg": 1, "m": 2, "s": -3}),
    "Pa": (Decimal("1"), {"kg": 1, "m": -1, "s": -2}),
    "V": (Decimal("1"), {"kg": 1, "m": 2, "s": -3, "A": -1}),
    "Ω": (Decimal("1"), {"kg": 1, "m": 2, "s": -3, "A": -2}),
    "ohm": (Decimal("1"), {"kg": 1, "m": 2, "s": -3, "A": -2}),
    "Hz": (Decimal("1"), {"s": -1}),
    "L": (Decimal("1"), {"L": 1}),
    "T": (Decimal("1"), {"T": 1}),
}
BASE_UNITS = {"kg", "m", "s", "A", "K", "mol", "rad", "L", "T"}


class ExerciseAttemptError(ValueError):
    pass


class ExerciseAttemptForbidden(PermissionError):
    pass


@dataclass(frozen=True)
class UnitParseResult:
    ok: bool
    scale: Decimal | None = None
    dimensions: dict[str, int] | None = None
    symbols: tuple[str, ...] = ()
    canonical_display: str = ""
    error: str | None = None

    def canonical_key(self):
        if not self.ok:
            return None
        return {
            "scale": str(self.scale.normalize()),
            "dimensions": dict(sorted((self.dimensions or {}).items())),
            "symbols": list(self.symbols),
            "display": self.canonical_display,
        }


def exercise_version(exercise):
    value = exercise.get("version", 1)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 1


def response_fields(exercise):
    interactions = exercise.get("interactions")
    fields = interactions if isinstance(interactions, list) and interactions else exercise.get("response_fields")
    if isinstance(fields, list) and fields:
        normalized_fields = []
        for index, field in enumerate(fields, start=1):
            if not isinstance(field, dict):
                continue
            normalized_field = dict(field)
            normalized_field["id"] = field.get("id") or f"response_{index}"
            normalized_field["type"] = field.get("type") or _response_mode_to_type(exercise.get("response_mode"))
            normalized_field["label"] = human_field_label(normalized_field)
            normalized_field.setdefault("input_help", field_input_help(normalized_field, exercise))
            normalized_fields.append(normalized_field)
        return normalized_fields

    response_mode = exercise.get("response_mode")
    if response_mode:
        response_type = _response_mode_to_type(response_mode)
        return [
            {
                "id": "response",
                "type": response_type,
                "label": "Respuesta",
                "prompt": exercise.get("response_prompt") or "Escribe tu respuesta.",
                "input_help": field_input_help({"type": response_type}, exercise),
            }
        ]

    return []


def _response_mode_to_type(response_mode):
    if response_mode == "numeric_multi":
        return "numeric"
    if response_mode in {"short_text", "written_upload"}:
        return response_mode
    return "open_text"


def field_map(exercise):
    return {str(field["id"]): field for field in response_fields(exercise)}


def response_map(attempt):
    return {response.field_id: response for response in attempt.responses}


def human_field_label(field):
    field_id = str(field.get("id", "")).strip()
    label = str(field.get("label") or field.get("prompt") or "").strip()
    if label and "_" not in label:
        return label
    fallback_labels = {
        "unit_derived": "Unidad usando N",
        "unit_base": "Unidad en unidades basicas",
        "force_factor": "Factor de cambio de la fuerza",
    }
    return fallback_labels.get(field_id, "Respuesta")


def field_input_help(field, exercise=None):
    if field.get("input_help"):
        return field.get("input_help")
    response_type = field.get("type")
    if response_type == "unit_expression":
        if field.get("unit_system") == "base_si" or field.get("id") == "unit_base":
            return "Escribela usando solo kg, m y s. Puedes usar espacios, * o / y exponentes."
        return "Puedes usar espacios, · o *. Se aceptan exponentes negativos o divisiones."
    if response_type == "numeric":
        if field.get("accepted_forms"):
            return "Se acepta la fraccion exacta o un decimal dentro de la tolerancia."
        return "Usa coma o punto decimal; tambien puedes usar notacion cientifica como 1.20e-3."
    if response_type == "single_choice":
        return "Elige una opcion."
    return None


def normalize_numeric_value(raw_value):
    value = (raw_value or "").strip()
    if not value:
        return None

    compact = value.replace(" ", "")
    fraction_match = FRACTION_RE.match(compact)
    if fraction_match:
        numerator = _decimal_or_none(fraction_match.group(1).replace(",", "."))
        denominator = _decimal_or_none(fraction_match.group(2).replace(",", "."))
        if numerator is None or denominator in {None, Decimal("0")}:
            return None
        return format((numerator / denominator).normalize(), "f")

    if not NUMERIC_RE.match(compact):
        return None

    normalized = compact.replace(",", ".")
    try:
        number = Decimal(normalized)
    except InvalidOperation:
        return None

    return format(number.normalize(), "f")


def normalize_response(raw_value, response_type):
    if response_type == "numeric":
        return normalize_numeric_value(raw_value)
    if response_type == "unit_expression":
        parsed = parse_unit_expression(raw_value)
        return parsed.canonical_display if parsed.ok else (str(raw_value).strip() if raw_value is not None else "")
    if raw_value is None:
        return ""
    return str(raw_value).strip()


def normalize_unit_expression(raw_value):
    parsed = parse_unit_expression(raw_value)
    return parsed.canonical_display if parsed.ok else ""


def parse_unit_expression(raw_value):
    if raw_value is None or not str(raw_value).strip():
        return UnitParseResult(False, error="empty")
    parser = _UnitParser(str(raw_value))
    return parser.parse()


class _UnitParser:
    def __init__(self, raw_value):
        self.cleaned = _prepare_unit_expression(raw_value)
        self.tokens = UNIT_TOKEN_RE.findall(self.cleaned)
        self.position = 0

    def parse(self):
        compact = self.cleaned.replace(" ", "")
        if not self.tokens or "".join(self.tokens) != compact:
            return UnitParseResult(False, error="unsupported notation")
        scale, dimensions, symbols = self._expression()
        if scale is None or self.position != len(self.tokens):
            return UnitParseResult(False, error="malformed expression")
        dimensions = {key: value for key, value in dimensions.items() if value}
        symbols = tuple(dict.fromkeys(symbols))
        return UnitParseResult(True, scale, dimensions, symbols, _format_unit_dimensions(dimensions))

    def _expression(self):
        scale, dimensions, symbols = self._factor()
        if scale is None:
            return None, {}, []
        while self._peek() in {"*", "/"} or self._starts_implicit_factor():
            operator = self._peek()
            if operator in {"*", "/"}:
                self.position += 1
            else:
                operator = "*"
            right_scale, right_dimensions, right_symbols = self._factor()
            if right_scale is None:
                return None, {}, []
            power = -1 if operator == "/" else 1
            scale *= right_scale ** power
            dimensions = _combine_dimensions(dimensions, right_dimensions, power)
            symbols.extend(right_symbols)
        return scale, dimensions, symbols

    def _factor(self):
        token = self._peek()
        if token == "(":
            self.position += 1
            scale, dimensions, symbols = self._expression()
            if self._peek() != ")":
                return None, {}, []
            self.position += 1
        elif token in UNIT_DEFINITIONS:
            self.position += 1
            scale, dimensions = UNIT_DEFINITIONS[token]
            dimensions = dict(dimensions)
            symbols = [token]
        else:
            return None, {}, []

        exponent = self._optional_exponent()
        if exponent != 1:
            scale = scale ** exponent
            dimensions = {key: value * exponent for key, value in dimensions.items()}
        return scale, dimensions, symbols

    def _optional_exponent(self):
        if self._peek() == "^":
            self.position += 1
            sign = 1
            if self._peek() in {"+", "-"}:
                if self._peek() == "-":
                    sign = -1
                self.position += 1
            if self._peek() and self._peek().isdigit():
                value = int(self._peek())
                self.position += 1
                return sign * value
            return 1
        if self._peek() in {"+", "-"}:
            sign = -1 if self._peek() == "-" else 1
            self.position += 1
            if self._peek() and self._peek().isdigit():
                value = int(self._peek())
                self.position += 1
                return sign * value
        return 1

    def _starts_implicit_factor(self):
        return self._peek() == "(" or self._peek() in UNIT_DEFINITIONS

    def _peek(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]


def _prepare_unit_expression(raw_value):
    value = str(raw_value).strip()
    superscripts = {
        "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
        "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
        "⁻": "-", "⁺": "+",
        "Â¹": "1", "Â²": "2", "Â³": "3", "â»": "-",
    }

    def expand_superscript(match):
        exponent = match.group(2)
        for old, new in superscripts.items():
            exponent = exponent.replace(old, new)
        return f"{match.group(1)}^{exponent}"

    value = re.sub(r"([A-Za-zΩ]+)((?:⁻|⁺|[⁰¹²³⁴⁵⁶⁷⁸⁹]|â»|Â¹|Â²|Â³)+)", expand_superscript, value)
    value = value.replace("Â·", "*").replace("·", "*").replace("Î©", "Ω")
    value = value.replace("Â¹", "^1").replace("Â²", "^2").replace("Â³", "^3")
    value = value.replace("¹", "^1").replace("²", "^2").replace("³", "^3")
    value = value.replace("â»", "-").replace("⁻", "-")
    value = re.sub(r"([A-Za-zΩ]+)([-+]\d+)", r"\1^\2", value)
    value = value.replace("**", "^")
    value = value.replace("[", "").replace("]", "")
    return re.sub(r"\s+", " ", value)


def _combine_dimensions(left, right, right_power=1):
    combined = dict(left)
    for key, value in right.items():
        combined[key] = combined.get(key, 0) + value * right_power
        if combined[key] == 0:
            combined.pop(key)
    return combined


def _format_unit_dimensions(dimensions):
    if not dimensions:
        return "1"
    order = ["kg", "m", "s", "A", "K", "mol", "rad", "L", "T"]
    parts = []
    for symbol in order:
        exponent = dimensions.get(symbol)
        if not exponent:
            continue
        parts.append(symbol if exponent == 1 else f"{symbol}^{exponent}")
    return " ".join(parts)


def start_or_resume_attempt(username, exercise):
    if not username:
        raise ExerciseAttemptForbidden("Authentication is required.")

    version = exercise_version(exercise)
    attempt = (
        ExerciseAttempt.query.filter_by(
            username=username,
            exercise_id=str(exercise["id"]),
            exercise_version=version,
            status=ATTEMPT_STARTED,
        )
        .order_by(ExerciseAttempt.updated_at.desc())
        .first()
    )
    if attempt:
        mark_exercise_worked(username, exercise)
        return attempt, False

    attempt = ExerciseAttempt(
        username=username,
        exercise_id=str(exercise["id"]),
        exercise_version=version,
        status=ATTEMPT_STARTED,
        started_at=utc_now(),
        updated_at=utc_now(),
        active_duration_seconds=0,
        timer_enabled=True,
        timer_paused=False,
    )
    db.session.add(attempt)
    db.session.commit()
    mark_exercise_worked(username, exercise)
    record_activity_event(
        username,
        "exercise_started",
        "exercise",
        object_id=exercise["id"],
        object_title=exercise.get("title"),
        metadata={"attempt_id": attempt.id, "exercise_version": version},
    )
    return attempt, True


def get_owned_attempt(username, attempt_id):
    attempt = db.session.get(ExerciseAttempt, attempt_id)
    if attempt is None:
        raise ExerciseAttemptError("Attempt not found.")
    if attempt.username != username:
        raise ExerciseAttemptForbidden("Attempt belongs to another user.")
    return attempt


def latest_started_attempt(username, exercise):
    return (
        ExerciseAttempt.query.filter_by(
            username=username,
            exercise_id=str(exercise["id"]),
            exercise_version=exercise_version(exercise),
            status=ATTEMPT_STARTED,
        )
        .order_by(ExerciseAttempt.updated_at.desc())
        .first()
    )


def get_catalogue_attempt_summaries(username, exercises):
    if not username or not exercises:
        return {}

    ids = [str(exercise.get("id")) for exercise in exercises if exercise.get("id")]
    attempts = (
        ExerciseAttempt.query.filter(
            ExerciseAttempt.username == username,
            ExerciseAttempt.exercise_id.in_(ids),
        )
        .order_by(ExerciseAttempt.updated_at.desc(), ExerciseAttempt.id.desc())
        .all()
    )

    summaries = {
        exercise_id: {
            "status": "new",
            "label": "Nuevo",
            "started_attempt": None,
            "latest_attempt": None,
            "latest_submitted_attempt": None,
            "submitted_count": 0,
        }
        for exercise_id in ids
    }

    for attempt in attempts:
        summary = summaries.setdefault(
            attempt.exercise_id,
            {
                "status": "new",
                "label": "Nuevo",
                "started_attempt": None,
                "latest_attempt": None,
                "latest_submitted_attempt": None,
                "submitted_count": 0,
            },
        )
        if summary["latest_attempt"] is None:
            summary["latest_attempt"] = attempt
        if attempt.status == ATTEMPT_STARTED and summary["started_attempt"] is None:
            summary["started_attempt"] = attempt
        if attempt.status in {ATTEMPT_SUBMITTED, ATTEMPT_REVIEWED}:
            summary["submitted_count"] += 1
            if summary["latest_submitted_attempt"] is None:
                summary["latest_submitted_attempt"] = attempt

    for summary in summaries.values():
        if summary["started_attempt"] is not None:
            summary["status"] = ATTEMPT_STARTED
            summary["label"] = "En progreso"
        elif summary["submitted_count"]:
            summary["status"] = "completed"
            summary["label"] = "Completado"

    return summaries


def next_exercise_after(exercise, exercises):
    current_id = str(exercise.get("id"))
    same_topic = [
        item
        for item in exercises
        if item.get("course") == exercise.get("course") and item.get("topic") == exercise.get("topic")
    ]
    next_item = _next_after_id(current_id, same_topic)
    if next_item:
        return next_item

    same_course = [item for item in exercises if item.get("course") == exercise.get("course")]
    next_item = _next_after_id(current_id, same_course)
    if next_item:
        return next_item

    return _next_after_id(current_id, exercises)


def _next_after_id(current_id, exercises):
    for index, exercise in enumerate(exercises):
        if str(exercise.get("id")) == current_id:
            if index + 1 < len(exercises):
                return exercises[index + 1]
            return None
    return None


def save_draft(username, attempt_id, exercise, submitted_values):
    attempt = _validate_editable_attempt(username, attempt_id, exercise)
    _save_response_values(attempt, exercise, submitted_values, grade=False)
    attempt.status = ATTEMPT_STARTED
    attempt.updated_at = utc_now()
    db.session.commit()
    mark_exercise_worked(username, exercise)
    record_activity_event(
        username,
        "exercise_draft_saved",
        "exercise",
        object_id=attempt.exercise_id,
        object_title=exercise.get("title"),
        metadata={"attempt_id": attempt.id, "exercise_version": attempt.exercise_version},
    )
    return attempt


def submit_attempt(username, attempt_id, exercise, submitted_values):
    attempt = _validate_editable_attempt(username, attempt_id, exercise)
    timer_payload = submitted_values.pop("_timer", None)
    if timer_payload:
        _apply_timer_payload(attempt, timer_payload, allow_missing=True)
    _save_response_values(attempt, exercise, submitted_values, grade=True)

    graded = [
        response
        for response in attempt.responses
        if response.grading_status in {GRADE_CORRECT, GRADE_INCORRECT}
    ]
    attempt.score = float(sum(1 for response in graded if response.grading_status == GRADE_CORRECT))
    attempt.max_score = float(len(graded))
    attempt.status = ATTEMPT_SUBMITTED
    attempt.submitted_at = utc_now()
    attempt.updated_at = attempt.submitted_at
    db.session.commit()
    mark_exercise_worked(username, exercise)
    record_activity_event(
        username,
        "exercise_submitted",
        "exercise",
        object_id=attempt.exercise_id,
        object_title=exercise.get("title"),
        metadata={
            "attempt_id": attempt.id,
            "exercise_version": attempt.exercise_version,
            "score": attempt.score,
            "max_score": attempt.max_score,
        },
    )
    return attempt


def sync_attempt_timer(username, attempt_id, duration_seconds, timer_enabled=None, timer_paused=None):
    attempt = get_owned_attempt(username, attempt_id)
    if attempt.status != ATTEMPT_STARTED:
        raise ExerciseAttemptForbidden("Submitted attempts cannot update timing.")
    _apply_timer_payload(
        attempt,
        {"duration_seconds": duration_seconds, "timer_enabled": timer_enabled, "timer_paused": timer_paused},
        allow_missing=False,
    )
    attempt.updated_at = utc_now()
    db.session.commit()
    return attempt


def get_student_attempt_history(username):
    if not username:
        return []
    return (
        ExerciseAttempt.query.filter_by(username=username)
        .order_by(ExerciseAttempt.updated_at.desc(), ExerciseAttempt.id.desc())
        .all()
    )


def format_duration(seconds):
    if seconds is None:
        return None
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)
    if minutes:
        return f"{minutes:02d} min {remaining:02d} s"
    return f"{remaining:02d} s"


def attempt_correction_summary(attempt):
    responses = list(attempt.responses)
    correct = sum(1 for response in responses if response.grading_status == GRADE_CORRECT)
    incorrect = sum(1 for response in responses if response.grading_status == GRADE_INCORRECT)
    pending = sum(1 for response in responses if response.grading_status == GRADE_PENDING_REVIEW)
    corrected = correct + incorrect
    return {
        "correct": correct,
        "incorrect": incorrect,
        "pending": pending,
        "corrected": corrected,
        "provisional": pending > 0,
    }


def regrade_submitted_attempts(exercises_by_id, dry_run=True):
    changed = 0
    attempts_checked = 0
    attempts = ExerciseAttempt.query.filter(ExerciseAttempt.status.in_([ATTEMPT_SUBMITTED, ATTEMPT_REVIEWED])).all()
    for attempt in attempts:
        exercise = exercises_by_id.get(attempt.exercise_id)
        if not exercise or exercise_version(exercise) != attempt.exercise_version:
            continue
        attempts_checked += 1
        before = [
            (response.id, response.normalized_value, response.canonical_value, response.grading_status, response.auto_score)
            for response in attempt.responses
        ]
        _save_response_values(
            attempt,
            exercise,
            {response.field_id: response.raw_value or "" for response in attempt.responses},
            grade=True,
        )
        graded = [response for response in attempt.responses if response.grading_status in {GRADE_CORRECT, GRADE_INCORRECT}]
        attempt.score = float(sum(1 for response in graded if response.grading_status == GRADE_CORRECT))
        attempt.max_score = float(len(graded))
        after = [
            (response.id, response.normalized_value, response.canonical_value, response.grading_status, response.auto_score)
            for response in attempt.responses
        ]
        changed += sum(1 for old, new in zip(before, after) if old != new)
        if dry_run:
            db.session.rollback()
        else:
            db.session.commit()
    return {"attempts_checked": attempts_checked, "responses_changed": changed, "dry_run": dry_run}


def _validate_editable_attempt(username, attempt_id, exercise):
    attempt = get_owned_attempt(username, attempt_id)
    if attempt.exercise_id != str(exercise["id"]):
        raise ExerciseAttemptError("Attempt does not match this exercise.")
    if attempt.exercise_version != exercise_version(exercise):
        raise ExerciseAttemptError("Attempt version does not match this exercise.")
    if attempt.status != ATTEMPT_STARTED:
        raise ExerciseAttemptForbidden("Submitted attempts cannot be edited.")
    return attempt


def _save_response_values(attempt, exercise, submitted_values, grade):
    fields = field_map(exercise)
    response_by_field = response_map(attempt)

    unknown_fields = set(submitted_values) - set(fields)
    if unknown_fields:
        raise ExerciseAttemptError("Unknown response field.")

    for field_id, field in fields.items():
        raw_value = submitted_values.get(field_id, "")
        response_type = field.get("type") or "open_text"
        normalized_value = normalize_response(raw_value, response_type)

        response = response_by_field.get(field_id)
        if response is None:
            response = ExerciseResponse(attempt=attempt, field_id=field_id)
            db.session.add(response)

        response.response_type = response_type
        response.raw_value = raw_value
        response.normalized_value = normalized_value
        response.canonical_value = None
        response.updated_at = utc_now()

        if grade:
            _grade_response(response, field)
        else:
            response.grading_status = GRADE_UNGRADED
            response.auto_score = None
            response.feedback = None


def _grade_response(response, field):
    response_type = response.response_type

    if response_type == "vector" and field.get("expected_components"):
        raw = (response.raw_value or "").strip()
        components = raw[1:-1].split(';') if raw.startswith('(') and raw.endswith(')') else []
        values = [normalize_numeric_value(item) for item in components]
        expected = field['expected_components']
        tolerance = Decimal(str(field.get('tolerance', 0)))
        correct = len(values) == len(expected) and all(
            value is not None and abs(Decimal(value) - Decimal(str(target))) <= tolerance
            for value, target in zip(values, expected)
        )
        response.grading_status = GRADE_CORRECT if correct else GRADE_INCORRECT
        response.auto_score = 1.0 if correct else 0.0
        response.feedback = 'Componentes correctas.' if correct else 'Revisa las componentes y el formato (x; y).'
        return

    if response_type == "function" and (field.get("canonical_expression") or field.get("accepted_forms")):
        accepted = [field.get("canonical_expression"), *(field.get("accepted_forms") or [])]
        accepted = [str(value) for value in accepted if value]
        correct = any(_functions_equivalent(response.raw_value or "", expected) for expected in accepted)
        response.grading_status = GRADE_CORRECT if correct else GRADE_INCORRECT
        response.auto_score = 1.0 if correct else 0.0
        response.feedback = "Función equivalente aceptada." if correct else "Revisa la expresión y la variable indicada."
        return

    if response_type == "short_text" and field.get("accepted_forms"):
        given = _normalize_short_text(response.raw_value)
        accepted = {_normalize_short_text(value) for value in field.get("accepted_forms", [])}
        correct = bool(given) and given in accepted
        response.grading_status = GRADE_CORRECT if correct else GRADE_INCORRECT
        response.auto_score = 1.0 if correct else 0.0
        response.feedback = "Respuesta aceptada." if correct else "Revisa el término solicitado."
        return

    if response_type == "single_choice" and field.get("correct_option_id"):
        expected = str(field.get("correct_option_id"))
        is_correct = response.normalized_value == expected
        response.grading_status = GRADE_CORRECT if is_correct else GRADE_INCORRECT
        response.auto_score = 1.0 if is_correct else 0.0
        response.feedback = field.get("feedback_correct" if is_correct else "feedback_incorrect")
        return

    if response_type == "numeric" and field.get("expected_value") is not None:
        expected = _decimal_or_none(field.get("expected_value"))
        given = _decimal_or_none(response.normalized_value)
        tolerance = _decimal_or_none(field.get("tolerance", field.get("absolute_tolerance", field.get("abs_tolerance", 0))))
        accepted_forms = {
            normalize_numeric_value(str(form))
            for form in field.get("accepted_forms", [])
            if normalize_numeric_value(str(form)) is not None
        }
        if response.normalized_value in accepted_forms:
            is_correct = True
        elif expected is not None and given is not None and tolerance is not None:
            is_correct = abs(given - expected) <= tolerance
        else:
            response.grading_status = GRADE_PENDING_REVIEW if response.raw_value else GRADE_INCORRECT
            response.auto_score = None if response.grading_status == GRADE_PENDING_REVIEW else 0.0
            response.feedback = (
                "No hemos podido interpretar esta notacion con seguridad. Tu respuesta se ha conservado para revisarla."
                if response.grading_status == GRADE_PENDING_REVIEW
                else field.get("feedback_incorrect")
            )
            return
        response.grading_status = GRADE_CORRECT if is_correct else GRADE_INCORRECT
        response.auto_score = 1.0 if is_correct else 0.0
        response.feedback = field.get("feedback_correct" if is_correct else "feedback_incorrect")
        return

    if response_type == "unit_expression" and field.get("expected_value"):
        parsed_response = parse_unit_expression(response.raw_value)
        if not parsed_response.ok:
            if not response.raw_value:
                response.grading_status = GRADE_INCORRECT
                response.auto_score = 0.0
                response.feedback = field.get("feedback_incorrect")
            else:
                response.grading_status = GRADE_PENDING_REVIEW
                response.auto_score = None
                response.feedback = "No hemos podido interpretar esta notacion con seguridad. Tu respuesta se ha conservado para revisarla."
            return
        accepted = [parse_unit_expression(field.get("expected_value"))]
        accepted.extend(parse_unit_expression(form) for form in field.get("accepted_forms", []))
        accepted = [item for item in accepted if item.ok]
        response.canonical_value = json.dumps(parsed_response.canonical_key(), ensure_ascii=False, sort_keys=True)
        is_correct = any(_unit_equivalent(parsed_response, expected, field) for expected in accepted)
        response.grading_status = GRADE_CORRECT if is_correct else GRADE_INCORRECT
        response.auto_score = 1.0 if is_correct else 0.0
        if is_correct:
            response.feedback = field.get("feedback_correct") or "Forma equivalente aceptada."
        else:
            response.feedback = field.get("feedback_incorrect") or "La unidad no coincide con la forma pedida."
        return

    response.grading_status = GRADE_PENDING_REVIEW
    response.auto_score = None
    response.feedback = None


def _normalize_short_text(value):
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9+<>=:-]+", " ", text).strip()


def _functions_equivalent(given, expected):
    if _normalize_function_text(given) == _normalize_function_text(expected):
        return True
    given_tree = _safe_function_tree(given)
    expected_tree = _safe_function_tree(expected)
    if given_tree is None or expected_tree is None:
        return False
    variables = sorted(
        ({node.id for node in ast.walk(given_tree) if isinstance(node, ast.Name)} |
         {node.id for node in ast.walk(expected_tree) if isinstance(node, ast.Name)})
        - set(_FUNCTION_NAMES)
    )
    if len(variables) > 2:
        return False
    valid_points = 0
    for sample in (-3.25, -1.5, -0.4, 0.75, 2.0, 4.5):
        values = {name: sample + index * 0.37 for index, name in enumerate(variables)}
        try:
            left = _eval_function_tree(given_tree, values)
            right = _eval_function_tree(expected_tree, values)
        except (ArithmeticError, ValueError, TypeError):
            continue
        if not math.isfinite(left) or not math.isfinite(right):
            continue
        valid_points += 1
        if not math.isclose(left, right, rel_tol=1e-8, abs_tol=1e-8):
            return False
    return valid_points >= 3


_FUNCTION_NAMES = {
    "sin": math.sin, "sen": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "exp": math.exp, "pi": math.pi,
}
_FUNCTION_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.USub, ast.UAdd, ast.Constant, ast.Name, ast.Call, ast.Load,
)


def _normalize_function_text(value):
    return re.sub(r"\s+", "", str(value or "").casefold().replace("−", "-").replace("^", "**"))


def _safe_function_tree(value):
    text = _normalize_function_text(value).replace(",", ".")
    if not text or any(token in text for token in (";", "=", "<", ">")):
        return None
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError:
        return None
    if any(not isinstance(node, _FUNCTION_NODES) for node in ast.walk(tree)):
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and (not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTION_NAMES):
            return None
        if isinstance(node, ast.Name) and node.id.startswith("_"):
            return None
    return tree


def _eval_function_tree(tree, variables):
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            value = _FUNCTION_NAMES.get(node.id, variables.get(node.id))
            if callable(value) or value is None:
                raise ValueError("invalid bare name")
            return float(value)
        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            operations = {ast.Add: lambda: left + right, ast.Sub: lambda: left - right,
                          ast.Mult: lambda: left * right, ast.Div: lambda: left / right,
                          ast.Pow: lambda: left ** right}
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("invalid operation")
            return operation()
        if isinstance(node, ast.Call):
            return float(_FUNCTION_NAMES[node.func.id](*[evaluate(arg) for arg in node.args]))
        raise ValueError("invalid expression")

    return float(evaluate(tree))


def _unit_equivalent(given, expected, field):
    if given.dimensions != expected.dimensions:
        return False
    if not field.get("allow_scaled_equivalents") and given.scale != expected.scale:
        return False
    if field.get("unit_system") == "base_si" and any(symbol not in BASE_UNITS for symbol in given.symbols):
        return False
    return True


def _decimal_or_none(value):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def _apply_timer_payload(attempt, payload, allow_missing):
    if payload is None:
        if allow_missing:
            return
        raise ExerciseAttemptError("Timer payload is required.")
    try:
        duration = int(payload.get("duration_seconds", payload.get("active_duration_seconds")))
    except (TypeError, ValueError):
        raise ExerciseAttemptError("Timer duration must be a non-negative integer.") from None
    if duration < 0:
        raise ExerciseAttemptError("Timer duration must be non-negative.")
    current = attempt.active_duration_seconds
    if current is not None and duration < current:
        raise ExerciseAttemptError("Timer duration cannot move backwards.")
    if current is not None and duration - current > 12 * 60 * 60:
        raise ExerciseAttemptError("Timer duration jump is too large.")
    attempt.active_duration_seconds = duration
    if payload.get("timer_enabled") is not None:
        attempt.timer_enabled = _as_bool(payload.get("timer_enabled"))
    if payload.get("timer_paused") is not None:
        attempt.timer_paused = _as_bool(payload.get("timer_paused"))


def _as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}
