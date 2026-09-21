"""Small presentation layer; canonical source is plain text, never HTML."""

import re

from markupsafe import Markup, escape


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
