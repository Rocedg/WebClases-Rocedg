"""Small presentation layer; canonical source is plain text, never HTML."""

import re

from markupsafe import Markup, escape


def exercise_number(exercise):
    """Explicit `number` of an exercise record, else the numeric suffix of its ID."""
    if isinstance(exercise, dict):
        if exercise.get('number') is not None:
            return int(exercise['number'])
        exercise = exercise.get('id')
    match = re.search(r"_(\d+)$", str(exercise))
    return int(match.group(1)) if match else None


def render_exercise_source(source):
    # Keep multiline TeX together before interpreting paragraph/part boundaries.
    source = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)",
                    lambda match: match.group().replace("\n", " "), str(source), flags=re.S)
    sections = re.split(r"\n\s*\n|(?m:^(?=\([a-z]\)))", source)
    html = []
    in_list = False
    for section in sections:
        section = section.strip()
        if not section:
            continue
        part = re.match(r"\(([a-z])\)\s*(.*)", section, re.S)
        if part:
            if not in_list:
                html.append(Markup('<ol class="exercise-parts" type="a">'))
                in_list = True
            html.append(Markup('<li value="{}" data-part="{}">{}</li>').format(
                ord(part[1]) - ord('a') + 1, part[1], escape(part[2])))
        else:
            if in_list:
                html.append(Markup('</ol>'))
                in_list = False
            html.append(Markup('<p>{}</p>').format(escape(section)))
    if in_list:
        html.append(Markup('</ol>'))
    return Markup('').join(html)


def response_format_notes(fields):
    types = {field['type'] for field in fields}
    kinds = {field.get('response_kind') for field in fields}
    notes = []
    if 'numeric' in types or 'vector' in types:
        notes.append('Números: usa coma o punto decimal, fracciones como 2/3 o notación científica como 1.20e-3. Si la unidad aparece al lado, escribe solo el número.')
    if 'vector' in types or 'vector' in kinds:
        notes.append('Vectores: escribe las componentes en orden (x; y), separadas por punto y coma; por ejemplo (1,5; -2). La unidad aparece al lado.')
    if 'function' in types or 'function' in kinds:
        notes.append('Funciones: usa la variable indicada, * para multiplicar y ^ para potencias; por ejemplo 2*t^2 + 1.')
    if 'unit_expression' in types:
        notes.append('Unidades: Puedes usar espacios, * o / y exponentes, por ejemplo kg*m/s^2. Si se piden unidades básicas, usa kg, m y s.')
    if 'single_choice' in types:
        notes.append('Selección: marca una única opción por pregunta.')
    if any(f['type'] == 'short_text' and not f.get('response_kind') for f in fields):
        notes.append('Texto corto: escribe únicamente el término solicitado.')
    return notes


def response_placeholder(field):
    if field.get('placeholder'):
        return field['placeholder']
    if field['type'] == 'vector' or field.get('response_kind') == 'vector':
        return 'Ej.: (1,5; -2)'
    if field['type'] == 'function' or field.get('response_kind') == 'function':
        return 'Ej.: 2*t^2 + 1'
    return {'numeric': 'Ej.: 1,25', 'unit_expression': 'Ej.: kg*m/s^2'}.get(field['type'], 'Escribe tu respuesta')


def _format_number(value):
    """Spanish decimal comma, at most four significant figures, no trailing zeros."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return str(value)
    text = f"{value:.4g}"
    if "e" in text:
        mantissa, exponent = text.split("e")
        text = f"{mantissa}·10^{int(exponent)}"
    return text.replace(".", ",")


def expected_answer_text(field):
    """Plain-text expected answer of a response field, for the teacher's solution view."""
    field_type = field.get("type")
    unit = f" {field['unit']}" if field.get("unit") else ""
    if field_type == "numeric" and "expected_value" in field:
        text = _format_number(field["expected_value"]) + unit
        if field.get("tolerance") is not None:
            text += f" (tolerancia ±{_format_number(field['tolerance'])})"
        return text
    if field_type == "vector" and field.get("expected_components") is not None:
        components = "; ".join(_format_number(c) for c in field["expected_components"])
        return f"({components}){unit}"
    if field_type == "function" and field.get("canonical_expression"):
        variable = field.get("variable")
        text = field["canonical_expression"] + unit
        if variable:
            text = f"f({variable}) = {text}"
        if field.get("domain"):
            text += f", con {field['domain']}"
        return text
    if field_type == "single_choice" and field.get("correct_option_id"):
        for option in field.get("options") or []:
            if option.get("id") == field["correct_option_id"]:
                return option.get("label") or option["id"]
        return str(field["correct_option_id"])
    if field.get("accepted_forms"):
        return " · ".join(str(form) for form in field["accepted_forms"])
    return "Sin respuesta esperada registrada"
