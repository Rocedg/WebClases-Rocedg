"""Build the T0 v4 exercise bank from the editorial Markdown specification."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "content" / "exercises" / "1bach" / "t0" / "exercise-bank-t0-v4-spec.md"
OUTPUT_PATH = ROOT / "content" / "exercises" / "1bach" / "t0" / "exercises_t0.json"

FAMILY_BY_LETTER = {
    "U": ("units", "Lenguaje físico, unidades y análisis dimensional"),
    "V": ("vectors", "Vectores y elección de ejes"),
    "M": ("measurement", "Medida, error, incertidumbre y cifras significativas"),
    "C": ("calculus_graphs", "Funciones, gráficas, derivadas e integrales"),
}

MANDATORY_ASSETS = {
    "t0_v_012": "v012_punta_cola.svg",
    "t0_v_017": "v017_ejes_girados.svg",
    "t0_v_018": "v018_plano_inclinado.svg",
    "t0_v_024": "v024_entra_sale.svg",
    "t0_c_016": "c016_piecewise.svg",
    "t0_c_019": "c019_growth.svg",
    "t0_c_020": "c020_signed_area.svg",
}


def strip_inline_markup(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^\*\*([^*]+)\*\*:\s*", "", text)
    return text.strip()


def html_paragraph(text: str) -> str:
    text = text.strip().strip("«»")
    return f"<p>{text}</p>"


def solution_steps(solution: str) -> list[str]:
    solution = solution.strip()
    if not solution:
        return []
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ$])", solution) if part.strip()]
    if len(parts) <= 3:
        return parts
    return [" ".join(parts[:2]), " ".join(parts[2:-1]), parts[-1]]


def decimal_from_value(raw: str) -> float | None:
    value = raw.strip()
    value = re.sub(r"\([^)]*\)", "", value)
    value = value.replace(",", ".")
    if "/" in value:
        match = re.match(r"([+-]?\d+(?:\.\d+)?)\s*/\s*([+-]?\d+(?:\.\d+)?)", value)
        if match:
            return float(match.group(1)) / float(match.group(2))
    match = re.match(r"([+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)", value, re.I)
    if not match:
        return None
    return float(match.group(1))


def tolerance_from_text(text: str) -> float | None:
    match = re.search(r"tol\.\s*`?([0-9]+(?:[,.][0-9]+)?(?:e[+-]?[0-9]+)?)`?", text, re.I)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def significant_figures_from_text(text: str) -> int | None:
    match = re.search(r"(\d+)\s+cifras?", text, re.I)
    return int(match.group(1)) if match else None


def decimal_places_from_text(text: str) -> int | None:
    match = re.search(r"(\d+)\s+decimales?", text, re.I)
    return int(match.group(1)) if match else None


def accepted_forms_from_text(text: str) -> list[str]:
    forms: list[str] = []
    match = re.search(r"aceptar\s+([^.;)]+(?:\)|$))", text, re.I)
    if match:
        chunk = match.group(1).strip().rstrip(")")
        forms.extend([part.strip(" `") for part in re.split(r",|\bo\b", chunk) if part.strip(" `")])
    exact = re.search(r"([+-]?\d+\s*/\s*[+-]?\d+)", text)
    if exact:
        forms.append(exact.group(1).replace(" ", ""))
    return sorted(set(forms))


def split_field_pieces(raw: str) -> list[str]:
    pieces: list[str] = []
    current: list[str] = []
    depth = 0
    in_backtick = False
    for char in raw:
        if char == "`":
            in_backtick = not in_backtick
        elif not in_backtick and char == "(":
            depth += 1
        elif not in_backtick and char == ")" and depth:
            depth -= 1

        if char == ";" and depth == 0 and not in_backtick:
            piece = "".join(current).strip()
            if piece:
                pieces.append(piece)
            current = []
        else:
            current.append(char)

    piece = "".join(current).strip()
    if piece:
        pieces.append(piece)
    return pieces


def field_from_piece(piece: str, index: int) -> dict[str, Any]:
    piece = piece.strip().strip(".")
    field_id = f"response_{index}"
    label = piece
    expected_raw = ""

    if "=" in piece:
        left, right = piece.split("=", 1)
        field_id = re.sub(r"[^a-zA-Z0-9_]+", "_", left.strip().strip("`")).strip("_") or field_id
        expected_raw = right.strip()
        label = left.strip().strip("`").replace("_", " ")
    elif "texto" in piece.lower() or "justific" in piece.lower() or "explic" in piece.lower():
        field_id = re.sub(r"[^a-zA-Z0-9_]+", "_", piece.lower())[:36].strip("_") or field_id

    lower = piece.lower()
    field: dict[str, Any] = {
        "id": field_id,
        "label": label[:80],
        "required": True,
    }

    if "opciones" in lower or re.search(r"\bchoice\b|\bopci[oó]n\b|material|dominant|sign=", lower):
        field["type"] = "single_choice"
        option_match = re.search(r"opciones\s+([^.;]+)", piece, re.I)
        if option_match:
            option_ids = [item.strip(" `") for item in option_match.group(1).split(",")]
        elif field_id == "sign":
            option_ids = ["negative", "positive", "zero"]
        elif field_id == "dominant":
            option_ids = ["pressure", "height", "kinetic"]
        elif expected_raw and not decimal_from_value(expected_raw):
            option_ids = [expected_raw.split()[0].strip("`.,;")]
        else:
            option_ids = ["A", "B", "C", "D"]
        field["options"] = [{"id": option, "label": option} for option in option_ids if option]
        chosen = decimal_from_value(expected_raw)
        if expected_raw:
            field["correct_option_id"] = expected_raw.split()[0].strip("`.,;")
        return field

    numeric = decimal_from_value(expected_raw)
    if numeric is not None:
        field["type"] = "numeric"
        field["expected_value"] = numeric
        tol = tolerance_from_text(piece)
        field["tolerance"] = tol if tol is not None else 0.01
        if "tol." not in lower:
            field["tolerance_note"] = "Tolerancia añadida por contrato técnico al no estar explicitada en la línea abreviada del spec."
        sig = significant_figures_from_text(piece)
        if sig:
            field["significant_figures"] = sig
            field["prompt"] = f"Da el resultado con {sig} cifras significativas."
        dec = decimal_places_from_text(piece)
        if dec:
            field["decimal_places"] = dec
            field["prompt"] = f"Da el resultado con {dec} decimales."
        forms = accepted_forms_from_text(piece)
        if forms:
            field["accepted_forms"] = forms
        unit_source = re.sub(r"^`?[+-]?\d+(?:[,.]\d+)?(?:e[+-]?\d+)?`?", "", expected_raw, flags=re.I)
        unit_source = re.sub(r"^`?[+-]?\d+\s*/\s*[+-]?\d+`?", "", unit_source)
        unit_source = unit_source.split("(")[0].split(",")[0].strip(" `")
        if unit_source and not re.match(r"^(si|no|opciones)\b", unit_source, re.I):
            field["unit"] = unit_source
        return field

    if expected_raw and re.search(r"\b(unit|unidad|dimension|dimensi)", field_id, re.I):
        field["type"] = "unit_expression"
        field["expected_value"] = expected_raw.split("(")[0].strip().strip("`")
        forms = accepted_forms_from_text(piece)
        if forms:
            field["accepted_forms"] = forms
        return field

    field["type"] = "open_text"
    if expected_raw:
        field["expected_value"] = expected_raw.split("(")[0].strip()
        field["accepted_forms"] = accepted_forms_from_text(piece)
    return field


def parse_fields(raw: str, response_mode: str) -> list[dict[str, Any]]:
    raw = strip_inline_markup(raw)
    if not raw:
        return []
    if response_mode in {"written_upload", "written_solution"}:
        return [{"id": "written_solution", "label": "Desarrollo escrito o dibujo", "type": "written_upload", "required": True}]
    pieces = split_field_pieces(raw)
    return [field_from_piece(piece, index) for index, piece in enumerate(pieces, start=1)]


def exercise_sections(text: str) -> list[tuple[str, str, str]]:
    pattern = re.compile(r"^## (T0-[UVMC]-\d{3})\s+[—-]\s+(.+)$", re.M)
    matches = list(pattern.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n---\n\n# 4.", start)
        sections.append((match.group(1), match.group(2).strip(), text[start:end].strip()))
    return sections


def parse_exercise(public_id: str, title: str, body: str) -> dict[str, Any]:
    exercise_id = public_id.lower().replace("-", "_")
    letter = public_id.split("-")[1]
    family, block = FAMILY_BY_LETTER[letter]
    data: dict[str, str] = {}

    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        content = line[2:].strip()
        if content.startswith("**") and ":**" in content:
            key, value = content.split(":**", 1)
            data[key.strip("*").lower()] = value.strip()
        elif content.lower().startswith("**id:**"):
            data["id"] = content.split("**", 2)[-1].strip()

    id_match = re.search(r"\*\*ID:\*\*\s*`([^`]+)`", body)
    if id_match:
        exercise_id = id_match.group(1)

    diff_match = re.search(r"\*\*Dificultad / tiempo:\*\*\s*(\d+)\s*/\s*(\d+)", body, re.I)
    if not diff_match:
        diff_match = re.search(r"\*\*dificultad / tiempo:\*\*\s*(\d+)\s*/\s*(\d+)", body, re.I)
    difficulty = int(diff_match.group(1)) if diff_match else 3
    estimated = int(diff_match.group(2)) if diff_match else 10

    type_match = re.search(r"\*\*Tipo:\*\*\s*`?([^`\n.]+)`?", body, re.I)
    if not type_match:
        type_match = re.search(r"\*\*tipo:\*\*\s*`?([^`\n.]+)`?", body, re.I)
    response_mode = type_match.group(1).strip() if type_match else "open_text"

    statement_match = re.search(r"\*\*Enunciado:\*\*\s*(.+?)(?=\n- \*\*|\n\n)", body, re.S | re.I)
    statement = strip_inline_markup(statement_match.group(1).replace("\n", " ")) if statement_match else title

    fields_match = re.search(r"\*\*Campos:\*\*\s*(.+?)(?=\n- \*\*|\n\n)", body, re.S | re.I)
    if not fields_match:
        fields_match = re.search(r"\*\*Respuesta(?: esperada)?:\*\*\s*(.+?)(?=\n- \*\*|\n\n)", body, re.S | re.I)
    fields = parse_fields(fields_match.group(1).replace("\n", " ") if fields_match else "", response_mode)

    hint_match = re.findall(r"\*\*Pista \d+:\*\*\s*(.+)", body, re.I)
    if not hint_match:
        hints_line = re.search(r"\*\*Pistas:\*\*\s*(.+)", body, re.I)
        if hints_line:
            hint_match = [part.strip() for part in re.split(r";", hints_line.group(1)) if part.strip()]

    solution_match = re.search(r"\*\*Soluci[oó]n:\*\*\s*(.+?)(?=\n- \*\*|\n\n##|\Z)", body, re.S | re.I)
    if not solution_match:
        solution_match = re.search(r"\*\*Respuesta(?: esperada)?:\*\*\s*(.+?)(?=\n- \*\*|\n\n##|\Z)", body, re.S | re.I)
    solution_text = strip_inline_markup(solution_match.group(1).replace("\n", " ")) if solution_match else ""
    if not solution_text and fields_match:
        solution_text = "Respuestas indicadas por campos: " + strip_inline_markup(fields_match.group(1).replace("\n", " "))

    mistakes_match = re.search(r"\*\*Errores(?: a detectar)?:\*\*\s*(.+)", body, re.I)
    mistakes = []
    if mistakes_match:
        mistakes = [part.strip().strip(".") for part in re.split(r";", mistakes_match.group(1)) if part.strip()]

    assets: list[dict[str, str]] = []
    if exercise_id in MANDATORY_ASSETS:
        filename = MANDATORY_ASSETS[exercise_id]
        assets.append(
            {
                "path": f"static/exercises/1bach/t0/assets/{filename}",
                "alt": f"Diagrama obligatorio para {exercise_id}.",
                "description": re.sub(r"\s+", " ", re.search(r"Activo SVG obligatorio.*?(?=\n- \*\*Errores|\n\n##|\Z)", body, re.S | re.I).group(0)).strip()
                if re.search(r"Activo SVG obligatorio.*?(?=\n- \*\*Errores|\n\n##|\Z)", body, re.S | re.I)
                else f"Diagrama de apoyo para {title}.",
            }
        )

    return {
        "id": exercise_id,
        "title": title,
        "course": "1bach",
        "block": block,
        "topic": "t0",
        "concept": "Tema 0",
        "family": family,
        "subtype": response_mode,
        "difficulty": difficulty,
        "estimated_minutes": estimated,
        "response_mode": response_mode,
        "response_prompt": "Responde cada apartado en su campo. Usa coma decimal en la escritura visible y conserva las unidades indicadas.",
        "response_fields": fields,
        "statement": html_paragraph(statement),
        "assets": assets,
        "tags": ["t0", family, "version_4"],
        "interactions": fields,
        "origin": {"kind": "exercise_bank_t0_v4_spec", "source": "exercise-bank-t0-v4-spec.md"},
        "status": "active",
        "version": 4,
        "learning_objective": block,
        "common_mistakes": mistakes,
        "hints": hint_match,
        "solution": {"summary_steps": solution_steps(solution_text), "source": "exercise-bank-t0-v4-spec.md"},
    }


def build_bank() -> dict[str, Any]:
    text = SPEC_PATH.read_text(encoding="utf-8")
    exercises = [parse_exercise(public_id, title, body) for public_id, title, body in exercise_sections(text)]
    retired_ids = [
        "t0_u_017",
        "t0_u_018",
        *[f"t0_v_{number:03d}" for number in range(25, 37)],
        "t0_e_001",
        "t0_e_002",
        *[f"t0_c_{number:03d}" for number in range(21, 25)],
    ]
    return {
        "version": 4,
        "course": "1bach",
        "block": "Herramientas para empezar Física",
        "topic": "t0",
        "topic_slug": "t0",
        "description": "Banco editorial T0 versión 4 convertido desde exercise-bank-t0-v4-spec.md.",
        "retired_ids": retired_ids,
        "retired_exercises": [
            {
                "id": exercise_id,
                "title": f"{exercise_id} (retirado del banco activo T0 v4)",
                "version": 3,
                "status": "retired",
            }
            for exercise_id in retired_ids
        ],
        "exercises": exercises,
    }


def main() -> int:
    bank = build_bank()
    OUTPUT_PATH.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(bank['exercises'])} exercises.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
