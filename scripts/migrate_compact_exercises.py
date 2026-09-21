"""Migrate the visible T0-T2 banks to the compact exercise source format.

The default mode is read-only and reports the exact changes that would be made.
Pass ``--write`` to replace the three bank files after every validation succeeds.
The transformation is deterministic and idempotent; already migrated exercises
are left untouched.
"""

from __future__ import annotations

import argparse
import copy
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Any
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BANKS = (
    ROOT / "content/exercises/1bach/t0/exercises_t0.json",
    ROOT / "content/exercises/1bach/t1/exercises_t1.json",
    ROOT / "content/exercises/1bach/t2/exercises_t2.json",
)
OPEN_TYPES = {"open_text", "written_upload", "open_text", "text", "textarea", "numeric_or_expression_placeholder"}
PUBLISHED_STATUSES = {"active", "draft"}
STRUCTURED_TYPES = {"numeric", "unit_expression", "single_choice", "vector", "function", "short_text"}
SAFE_FUNCTION = re.compile(r"^[0-9A-Za-z_+*/^().,;=<>≤≥−\-\s]+$")
NUMBER = r"[+\-−]?\d+(?:[.,]\d+)?(?:[eE][+\-]?\d+)?"
FIELD_LABELS = {
    "unit_k": "Unidad de k", "k": "Constante k", "predicted_energy": "Energía predicha",
    "unit_rho": "Unidad de la resistividad", "quadrant": "Cuadrante",
    "no_derivable_en_x": "Punto no derivable (x)", "zero_time": "Instante de cambio de sentido",
    "positive_area": "Área positiva", "negative_signed": "Área negativa con signo",
    "displacement": "Desplazamiento", "distance": "Distancia",
}
EXERCISE_FIELD_LABELS = {
    ("t0_v_006", "C_D_paralelos_de_sentido_opuesto_y_D"): "Factor de proporcionalidad D/C",
    ("t0_v_006", "E_F_perpendiculares_porque_E_cdot_F"): "Producto escalar E·F",
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"p", "div", "br", "li"} and self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_text(value: str) -> str:
    parser = _TextExtractor()
    parser.feed(value)
    return unescape("".join(parser.parts)).strip()


def _protect_math(text: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def keep(match: re.Match[str]) -> str:
        key = f"MATHPLACEHOLDER{len(protected)}END"
        protected[key] = match.group(0)
        return key

    text = re.sub(
        r"\$([A-Za-z][A-Za-z0-9_]*)=\$\(([^)]*)\)\$",
        lambda m: keep(_SyntheticMatch(r"\(" + m.group(1) + "=(" + m.group(2) + r")\)")),
        text,
    )
    text = re.sub(
        r"([A-Za-z][A-Za-z0-9_]*)=\$\(([^)]*)\)\$",
        lambda m: keep(_SyntheticMatch(r"\(" + m.group(1) + "=(" + m.group(2) + r")\)")),
        text,
    )
    text = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", keep, text, flags=re.S)
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: keep(_SyntheticMatch(r"\[" + m.group(1).strip() + r"\]")), text, flags=re.S)
    text = re.sub(r"\$([^$\n]+?)\$", lambda m: keep(_SyntheticMatch(r"\(" + m.group(1).strip() + r"\)")), text)
    return text, protected


class _SyntheticMatch:
    def __init__(self, value: str) -> None:
        self.value = value

    def group(self, index: int = 0) -> str:
        return self.value


def mathify_plain_text(text: str) -> str:
    """Wrap conservative, unmistakable formula fragments from the generated banks."""
    text, protected = _protect_math(text)

    def wrap(value: str) -> str:
        key = f"MATHPLACEHOLDER{len(protected)}END"
        protected[key] = r"\(" + value.strip() + r"\)"
        return key

    unit = r"(?:m/s²|m/s|m·s⁻²|m·s⁻¹|rad/s²|rad/s|rad|km/h|km·h⁻¹|cm³|cm²|cm|mm|kg|g|N|J|Hz|s|m|°C|°)(?![A-Za-z])"
    lhs = r"(?:[A-Za-zα-ωΑ-Ω]+(?:_[A-Za-z0-9]+)?(?:\([^)]*\))?|\[[A-Za-zα-ωΑ-Ω]+\])"
    rhs = r"(?!MATHPLACEHOLDER)(?:[^\s;:.!?]|,(?=\d))+(?:\s*" + unit + r")?"
    equation = re.compile(r"(?<![\w\\])(" + lhs + r"\s*=\s*" + rhs + r")")
    text = equation.sub(lambda m: wrap(m.group(1).replace("sen", r"\sin")), text)
    text = re.sub(
        r"(?<![\w\\])(\([A-Za-z_,]+\)\s*=\s*\([^)]*\))",
        lambda m: wrap(m.group(1)), text,
    )
    text = re.sub(
        r"(?<![\w\\])(\((?:" + NUMBER + r")\s*[,;]\s*(?:" + NUMBER + r")(?:\s*[,;]\s*(?:" + NUMBER + r"))?\)(?:\s*" + unit + r")?)",
        lambda m: wrap(m.group(1)),
        text,
    )
    text = re.sub(r"(?<![\w\\])([+−-][xyz](?:′)?)(?!\w)", lambda m: wrap(m.group(1)), text)
    text = re.sub(r"(?<![\w\\])([A-Za-z]_[A-Za-z0-9]+)(?!\w)", lambda m: wrap(m.group(1)), text)
    text = re.sub(r"(?<![\w\\])([A-Za-z]\([A-Za-z0-9]+\))(?!\s*=)", lambda m: wrap(m.group(1)), text)
    text = re.sub(
        r"(?<![\w\\])((?:" + NUMBER + r")\s*(?:[A-Za-z°·⁻¹²³/]+)?(?:\s*[+−-]\s*(?:" + NUMBER + r")\s*(?:[A-Za-z°·⁻¹²³/]+)?)+)",
        lambda m: wrap(m.group(1)), text,
    )
    text = re.sub(r"(?<![\w\\])(\d+(?:[.,]\d+)?\s*[<≤]\s*[A-Za-z]\s*[<≤]\s*\d+(?:[.,]\d+)?)(?!\w)", lambda m: wrap(m.group(1)), text)
    for key, value in protected.items():
        text = text.replace(key, value)
    return text


def compact_source(value: str) -> str:
    text = html_to_text(value) if "<" in value and ">" in value else value.strip()
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"(?<!\w)\(?([a-f])\)\s*", lambda m: f"\n({m.group(1)}) ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = mathify_plain_text(text)
    return text.strip()


def clean_expected_text(value: Any) -> str:
    text = str(value or "").strip().strip("`").strip()
    return re.sub(r"[`]+$", "", text).strip()


def clean_label(field: dict[str, Any]) -> str:
    label = str(field.get("label") or "").strip()
    label = re.sub(r"`[^`]*`", "", label)
    label = re.sub(r"\s*=.*$", "", label)
    label = re.sub(r"\b(?:texto|explicación|justificación|desarrollo|dibujo|archivo)\b.*$", "", label, flags=re.I)
    label = label.replace("_", " ").strip(" `:;,.–-")
    label = label.replace("$", "").replace(r"\cdot", "·").strip()
    label = FIELD_LABELS.get(str(field.get("id")), label)
    if not label or len(label) < 2:
        label = str(field.get("id") or "Respuesta").replace("_", " ")
    replacements = {
        "response 1": "Primera respuesta", "response 2": "Segunda respuesta",
        "response 3": "Tercera respuesta", "response 4": "Cuarta respuesta",
        "response 5": "Quinta respuesta", "response 6": "Sexta respuesta",
        "func": "Función", "r": "Vector posición", "v": "Vector velocidad",
        "a": "Aceleración", "dr": "Desplazamiento", "vm": "Velocidad media",
    }
    return replacements.get(label.casefold(), label[:1].upper() + label[1:])[:90]


def clean_unit(value: Any) -> str | None:
    unit = str(value or "").strip()
    if not unit:
        return None
    if "$" in unit or "`" in unit:
        return None
    if "=" in unit or re.match(r"^/", unit):
        matches = re.findall(r"(?:m/s²|m/s|m·s⁻²|m·s⁻¹|rad/s|rad|kg/m³|g/cm³|cm³|cm²|km|cm|mm|kg|N|J|Pa|Hz|s|m|°|%)", unit)
        return matches[-1] if matches else None
    return unit


def tuple_from_label(label: str) -> list[float] | None:
    match = re.search(r"[(`]\s*(" + NUMBER + r")\s*[,;]\s*(" + NUMBER + r")\s*[)`]", label)
    if not match:
        return None
    return [float(part.replace(",", ".").replace("−", "-")) for part in match.groups()]


def can_be_function(field: dict[str, Any]) -> bool:
    forms = field.get("accepted_forms") or []
    canonical = field.get("canonical_expression")
    return field.get("response_kind") == "function" and bool(canonical or forms) and all(
        SAFE_FUNCTION.match(str(value)) for value in ([canonical] if canonical else []) + list(forms)
    )


def migrate_open_field(field: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    migrated = copy.deepcopy(field)
    migrated["label"] = clean_label(migrated)
    if can_be_function(migrated):
        migrated["type"] = "function"
        return migrated, "function"
    if migrated.get("expected_components") and isinstance(migrated["expected_components"], list):
        migrated["type"] = "vector"
        return migrated, "vector"
    raw_label = str(field.get("label") or "")
    label_tuple = tuple_from_label(raw_label)
    vector_words = re.search(r"\b(?:suma|resta|vector|velocidad|posición|desplazamiento|proyección|equilibrante)\b", raw_label, re.I)
    if label_tuple and vector_words and len(re.findall(r"[(`]\s*" + NUMBER + r"\s*[,;]\s*" + NUMBER, raw_label)) == 1:
        migrated["type"] = "vector"
        migrated["expected_components"] = label_tuple
        migrated.setdefault("component_order", ["x", "y"])
        migrated.setdefault("tolerance", 0.02)
        return migrated, "vector"
    expected = clean_expected_text(migrated.get("expected_value"))
    forms = [clean_expected_text(item) for item in migrated.get("accepted_forms", []) if clean_expected_text(item)]
    candidates = forms or ([expected] if expected else [])
    if candidates and max(map(len, candidates)) <= 48 and not any("=" in item for item in candidates):
        migrated["type"] = "short_text"
        migrated["accepted_forms"] = list(dict.fromkeys(candidates))
        migrated.pop("expected_value", None)
        return migrated, "short_text"
    return None, "removed_open"


def normalize_field(field: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    field_type = field.get("type") or "open_text"
    if field_type in OPEN_TYPES:
        result, action = migrate_open_field(field)
    else:
        result, action = copy.deepcopy(field), "kept"
    if result is None:
        return None, action
    if result.get("type") not in STRUCTURED_TYPES:
        return None, "removed_unsupported"
    result["label"] = clean_label(result)
    if result.get("unit") is not None:
        unit = clean_unit(result.get("unit"))
        if unit:
            result["unit"] = unit
        else:
            result.pop("unit", None)
    result.pop("input_help", None)
    return result, action


def part_letters(source: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"(?m)^\(([a-f])\)", source)))


def source_parts(source: str) -> dict[str, str]:
    pattern = re.compile(r"(?ms)^\(([a-f])\)\s*(.*?)(?=^\([a-f]\)|\Z)")
    return {match.group(1): match.group(2).strip() for match in pattern.finditer(source)}


def _search_tokens(value: str) -> set[str]:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    stop = {"calcula", "halla", "obtiene", "completa", "resultado", "respuesta", "final", "para", "desde", "entre", "sobre", "cada", "a", "e", "o", "u", "y"}
    tokens = set()
    for token in re.findall(r"[a-z0-9]+", value):
        if token in stop:
            continue
        if len(token) > 5 and token.endswith("es"):
            token = token[:-2]
        elif len(token) > 4 and token.endswith("s"):
            token = token[:-1]
        tokens.add(token)
    return tokens


def choose_part(field: dict[str, Any], index: int, total: int, source: str) -> str:
    parts = source_parts(source)
    if not parts:
        return "a"
    field_tokens = _search_tokens(
        f"{field.get('label', '')} {field.get('id', '')} "
        f"{'funcion dominio' if field.get('domain') else ''}"
    )
    scores = {letter: len(field_tokens & _search_tokens(question)) for letter, question in parts.items()}
    best_score = max(scores.values(), default=0)
    if best_score:
        winners = [letter for letter, score in scores.items() if score == best_score]
        if len(winners) == 1:
            return winners[0]
    letters = list(parts)
    target = min(len(letters) - 1, ((index + 1) * len(letters) - 1) // max(1, total))
    return letters[target]


def rewrite_parts(source: str, fields: list[dict[str, Any]]) -> str:
    by_part: dict[str, list[dict[str, Any]]] = {}
    for field in fields:
        by_part.setdefault(field["part"], []).append(field)
    if not part_letters(source):
        free_request = re.compile(r"\b(?:explica|justifica|dibuja|dibujo|representa|demuestra|comprueba|verifica|contrasta|discute|interpreta|clasifica|construye|usa)\b", re.I)
        sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", source) if item.strip()]
        kept = [sentence for sentence in sentences if not free_request.search(sentence)]
        if not kept:
            formulas = list(dict.fromkeys(re.findall(r"\\\(.*?\\\)", source)))
            source = "Datos: " + "; ".join(formulas) + "." if formulas else "Datos del ejercicio disponibles en los campos."
        else:
            source = " ".join(kept)
        labels = ", ".join(field["label"] for field in fields)
        return source.rstrip() + f"\n\n(a) Completa: {labels}."
    pattern = re.compile(r"(?ms)^\(([a-f])\)\s*(.*?)(?=^\([a-f]\)|\Z)")
    open_verbs = re.compile(r"\b(?:explica|justifica|dibuja|representa|demuestra|comprueba|verifica|contrasta|discute|interpreta|identifica|construye|por qué)\b", re.I)

    def replace(match: re.Match[str]) -> str:
        letter, question = match.group(1), match.group(2).strip()
        part_fields = by_part.get(letter)
        if not part_fields:
            return ""
        if open_verbs.search(question):
            labels = ", ".join(field["label"] for field in part_fields)
            verb = "Selecciona" if all(field["type"] == "single_choice" for field in part_fields) else "Completa"
            question = f"{verb}: {labels}."
        return f"({letter}) {question}\n"

    return pattern.sub(replace, source).strip()


def solution_text(exercise: dict[str, Any]) -> tuple[str, str | None]:
    solution = exercise.get("solution") if isinstance(exercise.get("solution"), dict) else {}
    steps = solution.get("summary_steps") or exercise.get("solution_steps") or []
    if isinstance(steps, str):
        steps = [steps]
    source = "\n\n".join(str(step).strip() for step in steps if str(step).strip())
    if not source and exercise.get("final_answer"):
        source = str(exercise["final_answer"])
    return compact_source(source), solution.get("source")


def migrate_exercise(exercise: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    if exercise.get("status") not in PUBLISHED_STATUSES:
        return copy.deepcopy(exercise)
    if "statement_source" in exercise:
        migrated = copy.deepcopy(exercise)
        migrated["statement_source"] = compact_source(migrated["statement_source"])
        migrated["solution_source"] = compact_source(migrated.get("solution_source", ""))
        return migrated
    migrated = copy.deepcopy(exercise)
    original_fields = migrated.get("response_fields") or migrated.get("interactions") or []
    statement = compact_source(str(migrated.get("statement") or ""))
    fields: list[dict[str, Any]] = []
    for index, field in enumerate(original_fields):
        normalized, action = normalize_field(field)
        report["field_actions"][action] = report["field_actions"].get(action, 0) + 1
        if normalized:
            normalized["label"] = EXERCISE_FIELD_LABELS.get((migrated["id"], normalized["id"]), normalized["label"])
            normalized["part"] = choose_part(normalized, index, len(original_fields), statement)
            if (
                normalized.get("type") == "vector" and fields and fields[-1].get("type") == "vector"
                and not (_search_tokens(normalized.get("label", "")) & set().union(*(
                    _search_tokens(question) for question in source_parts(statement).values()
                )))
            ):
                normalized["part"] = fields[-1]["part"]
            fields.append(normalized)

    if fields:
        statement = rewrite_parts(statement, fields)
    solution, reference = solution_text(migrated)
    migrated["statement_source"] = statement
    migrated["solution_source"] = solution
    if reference:
        migrated["solution_reference"] = reference
    migrated["response_fields"] = fields
    migrated["response_mode"] = "structured"
    migrated["response_prompt"] = "Responde los apartados en sus campos."
    for asset in migrated.get("assets", []):
        if isinstance(asset, dict) and re.search(r"Activo SVG|viewBox|serie[s]?\s", str(asset.get("description", "")), re.I):
            asset.pop("description", None)
    for key in ("statement", "solution", "solution_steps", "final_answer", "hints", "interactions"):
        migrated.pop(key, None)

    if not fields:
        migrated["status"] = "retired"
        migrated["retired_reason"] = "El ejercicio dependía por completo de respuestas abiertas sin corrección automática fiable."
        report["retired"].append({"id": migrated["id"], "title": migrated["title"], "reason": migrated["retired_reason"]})
    else:
        report["migrated"][migrated["topic"]] = report["migrated"].get(migrated["topic"], 0) + 1
    return migrated


def validate_bank(before: dict[str, Any], after: dict[str, Any], path: Path) -> None:
    before_exercises = before.get("exercises", [])
    after_exercises = after.get("exercises", [])
    if len(before_exercises) != len(after_exercises):
        raise ValueError(f"{path}: exercise count or order changed")
    for old, new in zip(before_exercises, after_exercises):
        for key in ("id", "version", "title", "course", "topic", "origin", "common_mistakes"):
            if old.get(key) != new.get(key):
                raise ValueError(f"{path}: {old.get('id')} changed protected metadata {key}")
        old_asset_paths = [asset if isinstance(asset, str) else asset.get("path") for asset in old.get("assets", [])]
        new_asset_paths = [asset if isinstance(asset, str) else asset.get("path") for asset in new.get("assets", [])]
        if old_asset_paths != new_asset_paths:
            raise ValueError(f"{path}: {old.get('id')} changed asset paths")
        if new.get("status") != "retired":
            if re.search(r"<[A-Za-z][^>]*>", new.get("statement_source", "")) or "$" in new.get("statement_source", ""):
                raise ValueError(f"{path}: {new['id']} has legacy statement markup")
            if not new.get("solution_source"):
                raise ValueError(f"{path}: {new['id']} has no solution source")
            for source_name in ("statement_source", "solution_source"):
                source = new.get(source_name, "")
                if re.search(r"<[A-Za-z][^>]*>", source) or "$" in source:
                    raise ValueError(f"{path}: {new['id']} has legacy markup in {source_name}")
                if source.count(r"\(") != source.count(r"\)") or source.count(r"\[") != source.count(r"\]"):
                    raise ValueError(f"{path}: {new['id']} has unbalanced math delimiters in {source_name}")
            fields = new.get("response_fields") or []
            if not fields or any(field.get("type") not in STRUCTURED_TYPES for field in fields):
                raise ValueError(f"{path}: {new['id']} has unstructured response fields")
            if any(not field.get("part") for field in fields):
                raise ValueError(f"{path}: {new['id']} has a field without part")
            if new.get("hints") or "interactions" in new:
                raise ValueError(f"{path}: {new['id']} retained hints or duplicate interactions")


def migrate_all(write: bool = False) -> dict[str, Any]:
    report: dict[str, Any] = {"migrated": {}, "retired": [], "field_actions": {}, "files": []}
    outputs: list[tuple[Path, dict[str, Any]]] = []
    for path in BANKS:
        before = json.loads(path.read_text(encoding="utf-8"))
        after = copy.deepcopy(before)
        after["exercises"] = [migrate_exercise(exercise, report) for exercise in before["exercises"]]
        validate_bank(before, after, path)
        # Round-trip validation happens before any file is written.
        serialized = json.dumps(after, ensure_ascii=False, indent=2) + "\n"
        json.loads(serialized)
        outputs.append((path, after))
        report["files"].append(str(path.relative_to(ROOT)))
    if write:
        for path, data in outputs:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write only after all banks pass validation.")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    args = parser.parse_args()
    report = migrate_all(write=args.write)
    report["mode"] = "write" if args.write else "check"
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Mode: {report['mode']}")
        print("Migrated: " + ", ".join(f"{key}={value}" for key, value in sorted(report["migrated"].items())))
        print(f"Retired: {len(report['retired'])}")
        for item in report["retired"]:
            print(f"- {item['id']}: {item['reason']}")
        print("Field actions: " + ", ".join(f"{key}={value}" for key, value in sorted(report["field_actions"].items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
