"""Build the T3-T6 compact exercise banks from their editorial Markdown tables.

The command is read-only by default. Pass --write to replace the generated JSON
and SVG assets after all validation checks pass.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "content" / "exercises" / "1bach"
ASSET_ROOT = ROOT / "static" / "exercises" / "1bach"
TOPICS = ("t3", "t4", "t5", "t6")

TOPIC_META = {
    "t3": {
        "concept": "Leyes de Newton",
        "description": "Fuerzas, diagramas de cuerpo libre y leyes de Newton aplicadas a sistemas y movimiento circular.",
        "families": {
            "f": ("Fuerzas e interacciones", 12),
            "n": ("Resultante y leyes de Newton", 12),
            "p": ("Planos, cuerdas y sistemas enlazados", 14),
            "c": ("Dinámica circular", 10),
            "i": ("Integración, diagnóstico y modelización", 12),
        },
    },
    "t4": {
        "concept": "Rozamiento y aplicaciones de las fuerzas",
        "description": "Rozamiento estático y cinético, curvas, muelles y selección razonada del modelo dinámico.",
        "families": {
            "r": ("Rozamiento estático y cinético", 16),
            "p": ("Planos con rozamiento", 12),
            "c": ("Curvas planas y peraltadas", 10),
            "m": ("Muelles y ley de Hooke", 12),
            "i": ("Experimento, integración y auditoría", 10),
        },
    },
    "t5": {
        "concept": "Energía y trabajo",
        "description": "Trabajo, potencia y balances de energía con gravedad, muelles y disipación.",
        "families": {
            "w": ("Trabajo y fuerzas variables", 14),
            "k": ("Energía cinética y potencia", 12),
            "g": ("Energía potencial gravitatoria", 10),
            "e": ("Energía elástica", 10),
            "b": ("Balances, disipación e integración", 14),
        },
    },
    "t6": {
        "concept": "Momento lineal, impulso y choques",
        "description": "Momento, impulso, sistemas, separaciones, choques y restitución.",
        "families": {
            "i": ("Momento e impulso", 12),
            "s": ("Sistemas y conservación", 10),
            "x": ("Separaciones y retroceso", 8),
            "c": ("Choques y restitución", 18),
            "a": ("Integración, gráficas y auditoría", 12),
        },
    },
}

UNIT_PATTERNS = (
    "kg·m/s", "kg m/s", "kg·m/s²", "kg m/s²", "kg·m²/s²", "kg·m²/s",
    "m/s²", "m/s", "N·s", "N/m", "N", "kN", "kW", "W", "kJ", "J",
    "kg", "m", "cm", "s", "rad", "°", "%",
)


def slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", normalized).strip("_").lower()
    return cleaned[:40] or "respuesta"


def compact_markup(value: str) -> str:
    value = value.strip().replace("→", r"\to ").replace("Δ", r"\Delta ")
    return re.sub(r"`([^`]+)`", lambda match: rf"\({match.group(1)}\)", value)


def plain_markup(value: str) -> str:
    return re.sub(r"`([^`]+)`", r"\1", value).replace("**", "").strip()


def parse_rows(topic: str) -> list[dict[str, str]]:
    path = COURSE_ROOT / topic / f"referencia-ejercicios-{topic}.md"
    rows: list[dict[str, str]] = []
    row_pattern = re.compile(rf"^\| `({topic}_[a-z]_\d{{3}})` \| (.*?) \| (.*?) \| (.*?) \|$")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = row_pattern.match(line)
        if match:
            rows.append({"id": match.group(1), "activity": match.group(2), "key": match.group(3), "visual": match.group(4)})
    return rows


def numeric_value(text: str) -> float:
    return float(text.replace("−", "-").replace(",", "."))


def unit_from(text: str) -> str:
    normalized = text.replace(" ", "")
    for unit in UNIT_PATTERNS:
        if unit.replace(" ", "") in normalized:
            return unit
    return ""


def numeric_fields(key: str) -> list[dict[str, Any]]:
    spans = list(re.finditer(r"`([^`]+)`", key))
    fields: list[dict[str, Any]] = []
    used: Counter[str] = Counter()
    vector_pattern = re.compile(r"\(\s*([−+\-]?\d+(?:[,.]\d+)?)\s*;\s*([−+\-]?\d+(?:[,.]\d+)?)\s*\)")
    final_number = re.compile(r"(?:=|^|:)\s*([−+\-]?\d+(?:[,.]\d+)?)(?!.*[=;])")

    for span_index, span_match in enumerate(spans, start=1):
        span = span_match.group(1)
        if key[span_match.end():].lstrip().startswith(":"):
            continue
        vector = vector_pattern.search(span)
        if vector:
            label = plain_markup(span.split("=")[0]) if "=" in span else "Vector"
            field_id = unique_id(slug(label), used)
            fields.append({
                "id": field_id,
                "label": label,
                "type": "vector",
                "response_kind": "vector",
                "required": True,
                "expected_components": [numeric_value(vector.group(1)), numeric_value(vector.group(2))],
                "accepted_forms": [f"({vector.group(1)}; {vector.group(2)})"],
                "component_order": ["x", "y"],
                "unit": unit_from(span),
                "tolerance": 0.02,
            })
            continue

        match = final_number.search(span)
        if not match:
            continue
        suffix = span[match.end():].strip()
        # A coefficient followed by a variable is an expression, not a numeric answer.
        suffix_without_unit = suffix
        for known_unit in UNIT_PATTERNS:
            suffix_without_unit = suffix_without_unit.replace(known_unit, "")
        if re.search(r"[A-Za-zθμω]", suffix_without_unit) or any(char in suffix for char in "²³") and not unit_from(suffix):
            continue
        # Reject input-like intervals, ratios and formula coefficients unless the span states a result.
        if any(token in span for token in ("≤", "≥", "∝")) and "=" not in span:
            continue
        value = numeric_value(match.group(1))
        label = plain_markup(span.split("=")[0]).strip(" :") if "=" in span else inferred_label(key, span_match.start(), span_index)
        label = pretty_label(label)
        if label.replace("-", "").replace("+", "").replace(",", "").replace(".", "").isdigit():
            label = f"Resultado {span_index}"
        field_id = unique_id(slug(label), used)
        unit = unit_from(span[match.end():]) or unit_from(span)
        tolerance = 0.2 if unit == "°" else max(0.01, abs(value) * 0.005)
        fields.append({
            "id": field_id,
            "label": label or "Resultado",
            "type": "numeric",
            "required": True,
            "expected_value": value,
            "unit": unit,
            "tolerance": tolerance,
            "significant_figures": 3,
        })

    resolved = deduplicate_numeric(fields)
    label_counts = Counter(field["label"] for field in resolved)
    label_seen: Counter[str] = Counter()
    for field in resolved:
        label = field["label"]
        if label_counts[label] > 1:
            label_seen[label] += 1
            field["label"] = f"{label} {label_seen[label]}"
    known_units = {field.get("unit") for field in resolved if field.get("unit")}
    if len(known_units) == 1:
        shared_unit = next(iter(known_units))
        for field in resolved:
            if field["type"] == "numeric" and not field.get("unit"):
                field["unit"] = shared_unit
    return resolved


def inferred_label(key: str, start: int, index: int) -> str:
    prefix = re.sub(r"`[^`]+`", "", key[:start])
    fragment = re.split(r"[;.]", prefix)[-1].strip(" :,()")
    fragment = re.sub(r"^(?:y|con|resultado|valor|valores)\s+", "", fragment, flags=re.I)
    if not fragment:
        return f"Resultado {index}"
    candidate = " ".join(fragment.split()[-4:]).capitalize()
    if candidate.lower() in {"momentos", "trabajos", "aceleraciones", "energías", "fuerzas"}:
        candidate = candidate[:-1] + f" {index}"
    return candidate[:48]


def pretty_label(label: str) -> str:
    mappings = {
        "T": "Tensión", "N": "Normal", "a": "Aceleración", "v": "Rapidez",
        "p": "Momento lineal", "W": "Trabajo", "K": "Energía cinética",
        "U": "Energía potencial", "k_eq": "Constante equivalente",
        "v_1": "Velocidad final 1", "v_2": "Velocidad final 2",
        "u_1": "Velocidad inicial 1", "u_2": "Velocidad inicial 2",
        "f_k": "Rozamiento cinético", "f_s": "Rozamiento estático",
        "f_s,max": "Rozamiento estático máximo", "F_R": "Fuerza resultante",
    }
    return mappings.get(label, label.replace("_", " "))


def unique_id(base: str, used: Counter[str]) -> str:
    used[base] += 1
    return base if used[base] == 1 else f"{base}_{used[base]}"


def deduplicate_numeric(fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[tuple[Any, str, str]] = set()
    for field in fields:
        expected: Any = tuple(field["expected_components"]) if field["type"] == "vector" else field["expected_value"]
        marker = (expected, field.get("unit", ""), field["label"])
        if marker not in seen:
            seen.add(marker)
            result.append(field)
    return result[:5]


def conceptual_field(key: str, position: int) -> dict[str, Any] | None:
    lower = plain_markup(key).lower()
    groups = [
        (("perfectamente inelástico", "inelástico", "elástico", "superelástico"), ("perfectamente inelástico", "inelástico", "elástico", "superelástico"), "Tipo de interacción"),
        (("no desliza", "desliza", "reposo"), ("reposo", "desliza", "no desliza"), "Estado"),
        (("hacia arriba", "cuesta arriba", "arriba"), ("hacia arriba", "hacia abajo", "sin dirección preferente"), "Sentido"),
        (("hacia abajo", "cuesta abajo", "abajo"), ("hacia arriba", "hacia abajo", "sin dirección preferente"), "Sentido"),
        (("derecha",), ("derecha", "izquierda", "resultante nula"), "Sentido"),
        (("izquierda",), ("derecha", "izquierda", "resultante nula"), "Sentido"),
        (("tangente",), ("tangente", "radial hacia fuera", "paralela a la aceleración"), "Dirección vectorial"),
        (("radial",), ("radial hacia el centro", "tangente", "radial hacia fuera"), "Dirección vectorial"),
        (("se conserva", "constante"), ("se conserva", "aumenta necesariamente", "disminuye necesariamente"), "Conclusión"),
    ]
    for needles, options, label in groups:
        match = next((needle for needle in needles if re.search(rf"(?<!\w){re.escape(needle)}(?!\w)", lower)), None)
        if not match:
            continue
        correct = match
        if match in {"cuesta arriba", "arriba"}: correct = "hacia arriba"
        if match in {"cuesta abajo", "abajo"}: correct = "hacia abajo"
        if match == "radial": correct = "radial hacia el centro"
        if match == "constante": correct = "se conserva"
        option_list = [{"id": slug(option), "label": option.capitalize()} for option in dict.fromkeys(options)]
        return {
            "id": f"concepto_{position}",
            "label": label,
            "type": "single_choice",
            "required": True,
            "options": option_list,
            "correct_option_id": slug(correct),
        }
    return None


def fallback_field(key: str) -> dict[str, Any]:
    correct = plain_markup(key).rstrip(".")
    return {
        "id": "conclusion",
        "label": "Conclusión física",
        "type": "single_choice",
        "required": True,
        "options": [
            {"id": "modelo_correcto", "label": correct},
            {"id": "signo_opuesto", "label": "La magnitud relevante tiene siempre el signo opuesto."},
            {"id": "indeterminado", "label": "Los datos no permiten establecer ninguna relación."},
        ],
        "correct_option_id": "modelo_correcto",
    }


def build_fields(key: str) -> list[dict[str, Any]]:
    fields = numeric_fields(key)
    conceptual = conceptual_field(key, len(fields) + 1)
    if conceptual and len(fields) < 5:
        fields.append(conceptual)
    if not fields:
        fields.append(fallback_field(key))
    letters = "abcde"
    for index, field in enumerate(fields):
        field["part"] = letters[index]
        if field["type"] == "numeric":
            field["rounding"] = "Tres cifras significativas; conservar precisión intermedia."
    return fields


def exercise_title(activity: str) -> str:
    title = plain_markup(re.sub(r"`[^`]*=[^`]*`", "", activity))
    title = re.sub(r"(?:^|,?\s+)[A-Za-zθμω][A-Za-z0-9_]*\s*=\s*[^,;.]+", "", title)
    title = title.strip(" ,")
    title = re.split(r"[:;.]", title, maxsplit=1)[0]
    if not title:
        title = "Problema estructurado"
    title = title[0].upper() + title[1:]
    return title[:76].rstrip(" ,")


def difficulty(topic: str, family: str, number: int, count: int) -> int:
    ratio = number / count
    base = 2 if family in {"f", "n", "r", "w", "k", "g", "i", "s"} else 3
    if ratio > 0.82: return min(5, base + 2)
    if ratio > 0.42: return min(5, base + 1)
    return base


def estimated_minutes(level: int, field_count: int) -> int:
    return min(18, 4 + 2 * level + field_count)


def build_exercise(topic: str, row: dict[str, str]) -> dict[str, Any]:
    exercise_id = row["id"]
    family = exercise_id.split("_")[1]
    number = int(exercise_id.rsplit("_", 1)[1])
    block, count = TOPIC_META[topic]["families"][family]
    fields = build_fields(row["key"])
    questions = []
    for field in fields:
        verb = "Selecciona" if field["type"] == "single_choice" else "Calcula"
        questions.append(f"({field['part']}) {verb}: {field['label']}.")
    statement = compact_markup(row["activity"]) + "\n\n" + "\n".join(questions)
    level = difficulty(topic, family, number, count)
    visual_path = f"static/exercises/1bach/{topic}/assets/{exercise_id}.svg"
    return {
        "id": exercise_id,
        "version": 1,
        "title": exercise_title(row["activity"]),
        "course": "1bach",
        "topic": topic,
        "concept": TOPIC_META[topic]["concept"],
        "block": block,
        "family": family,
        "subtype": "multi_step",
        "difficulty": level,
        "estimated_minutes": estimated_minutes(level, len(fields)),
        "response_mode": "structured",
        "response_prompt": "Responde los apartados en sus campos.",
        "response_fields": fields,
        "assets": [{"path": visual_path, "alt": plain_markup(row["visual"])}],
        "tags": [topic, family, "comprension", "diagrama", "original"],
        "origin": {"kind": "original_teacher_bank", "reference": None, "adaptation_note": "Enunciado, datos, solución y diagrama propios."},
        "status": "draft",
        "learning_objective": f"{block}: conectar la representación con el modelo físico y comprobar el resultado.",
        "prerequisites": ["T0: unidades, signos y álgebra", block],
        "difficulty_reason": "Exige identificar el modelo, leer el diagrama y coordinar varios resultados verificables.",
        "common_mistakes": common_mistakes(topic, family),
        "parts_count": len(fields),
        "statement_source": statement,
        "solution_source": compact_markup(row["key"]) + "\n\nLa comprobación debe respetar signos, unidades, sistema elegido y coherencia con el diagrama.",
        "solution_reference": f"referencia-ejercicios-{topic}.md; elaboración propia y revisión matemática.",
    }


def common_mistakes(topic: str, family: str) -> list[str]:
    by_topic = {
        "t3": ["añadir la resultante como una fuerza independiente", "confundir acción-reacción con fuerzas sobre el mismo cuerpo"],
        "t4": ["usar siempre el rozamiento estático máximo", "elegir el sentido del rozamiento sin analizar la tendencia"],
        "t5": ["confundir trabajo transferido con energía almacenada", "sumar dos veces una interacción conservativa"],
        "t6": ["conservar el momento de un objeto aislado durante el choque", "conservar energía cinética en cualquier interacción"],
    }
    return by_topic[topic] + [f"ignorar la representación específica de la familia {family}"]


def svg_for(exercise: dict[str, Any], visual: str) -> str:
    topic, family = exercise["topic"], exercise["family"]
    title = html.escape(exercise["title"])
    desc = html.escape(plain_markup(visual))
    body = svg_body(topic, family, plain_markup(visual).lower())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-labelledby="title desc" style="max-width:100%;height:auto">
  <title id="title">{title}</title><desc id="desc">{desc}</desc>
  <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="context-stroke"/></marker></defs>
  <rect width="640" height="360" fill="#fff"/>
  <g font-family="Arial,sans-serif" fill="#203148" stroke-linecap="round" stroke-linejoin="round">
    {body}
  </g>
</svg>\n'''


def arrow(x1: int, y1: int, x2: int, y2: int, label: str, color: str = "#2766d8") -> str:
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="3" marker-end="url(#arrow)"/><text x="{x2+8}" y="{y2}" font-size="15" fill="{color}">{label}</text>'


def axes() -> str:
    return '<path d="M70 285H580M110 320V55" stroke="#68788b" stroke-width="1.6" marker-end="url(#arrow)"/><text x="585" y="305">x</text><text x="122" y="60">y</text>'


def svg_body(topic: str, family: str, visual: str) -> str:
    if topic == "t3" and family in {"f", "n"}:
        return f'<rect x="255" y="145" width="130" height="80" rx="8" fill="#edf4ff" stroke="#245b99" stroke-width="2"/>{arrow(320,145,320,70,"N")}{arrow(320,225,320,305,"P","#ba513c")}{arrow(385,185,505,185,"F")}{arrow(255,185,175,185,"f","#7b5ab5")}<text x="270" y="190" font-size="16">sistema</text>'
    if topic == "t3" and family == "p":
        return f'<path d="M90 285H555L235 105Z" fill="#f3f6fa" stroke="#68788b" stroke-width="2"/><rect x="272" y="160" width="82" height="58" rx="6" fill="#edf4ff" stroke="#245b99" stroke-width="2" transform="rotate(29 313 189)"/>{arrow(313,188,313,290,"P","#ba513c")}{arrow(313,188,374,82,"N")}<circle cx="530" cy="105" r="27" fill="none" stroke="#68788b" stroke-width="3"/><path d="M354 160L510 105V250" fill="none" stroke="#7b5ab5" stroke-width="2"/>'
    if topic == "t3" and family == "c":
        if "cono" in visual or "péndulo" in visual:
            return f'<path d="M320 55V90" stroke="#68788b" stroke-width="3"/><path d="M320 90L430 230" stroke="#245b99" stroke-width="3"/><ellipse cx="320" cy="230" rx="110" ry="42" fill="#f7faff" stroke="#b8c3d0" stroke-width="2" stroke-dasharray="7 6"/><circle cx="430" cy="230" r="15" fill="#ba513c"/>{arrow(430,230,350,128,"T")}{arrow(430,230,430,315,"P","#ba513c")}<path d="M320 90V230" stroke="#b8c3d0" stroke-dasharray="7 6"/><text x="330" y="135">θ</text>'
        return f'<circle cx="320" cy="190" r="105" fill="#f7faff" stroke="#245b99" stroke-width="2"/><circle cx="320" cy="190" r="5"/>{arrow(425,190,330,190,"radial","#ba513c")}{arrow(425,190,425,85,"tangente")}<path d="M388 112A105 105 0 0 1 423 166" fill="none" stroke="#7b5ab5" stroke-width="3" marker-end="url(#arrow)"/>'
    if topic == "t3":
        return axes() + '<rect x="180" y="125" width="115" height="70" fill="#edf4ff" stroke="#245b99"/><rect x="395" y="125" width="115" height="70" fill="#fff4e8" stroke="#ba513c"/><path d="M295 160H390" stroke="#7b5ab5" stroke-width="3" marker-end="url(#arrow)"/><text x="207" y="165">sistema</text><text x="423" y="165">modelo</text>'
    if topic == "t4" and family == "r":
        return f'<path d="M75 255H565" stroke="#68788b" stroke-width="4"/><rect x="245" y="170" width="145" height="82" rx="7" fill="#fff4e8" stroke="#ba513c" stroke-width="2"/>{arrow(390,210,520,210,"F")}{arrow(245,225,145,225,"f","#7b5ab5")}<path d="M120 275h400" stroke="#b8c3d0" stroke-dasharray="8 6"/>'
    if topic == "t4" and family == "p":
        return f'<path d="M80 290H570L220 90Z" fill="#f5f7fa" stroke="#68788b" stroke-width="2"/><rect x="286" y="162" width="95" height="62" fill="#fff4e8" stroke="#ba513c" transform="rotate(29 333 193)"/>{arrow(333,190,260,230,"f","#7b5ab5")}{arrow(333,190,395,83,"N")}'
    if topic == "t4" and family == "c":
        return '<path d="M85 275Q320 55 555 275" fill="none" stroke="#68788b" stroke-width="40"/><path d="M85 275Q320 55 555 275" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="12 10"/><circle cx="320" cy="125" r="18" fill="#ba513c"/><path d="M320 125L320 250" stroke="#245b99" stroke-width="3" marker-end="url(#arrow)"/><text x="330" y="205">hacia el centro</text>'
    if topic == "t4" and family == "m":
        if "paralelo" in visual:
            return '<path d="M75 75V290" stroke="#68788b" stroke-width="8"/><path d="M75 135h45l20-18 25 36 25-36 25 36 25-18h40M75 235h45l20-18 25 36 25-36 25 36 25-18h40" fill="none" stroke="#245b99" stroke-width="3"/><rect x="280" y="105" width="115" height="160" rx="8" fill="#edf4ff" stroke="#245b99" stroke-width="2"/><text x="130" y="95">k₁</text><text x="130" y="205">k₂</text><path d="M395 185H555" stroke="#b8c3d0" stroke-dasharray="7 6"/><text x="420" y="172">misma x</text>'
        return '<path d="M80 70V290" stroke="#68788b" stroke-width="8"/><path d="M80 180l25-20 25 40 25-40 25 40 25-40 25 20" fill="none" stroke="#245b99" stroke-width="3"/><rect x="230" y="135" width="115" height="90" rx="8" fill="#edf4ff" stroke="#245b99" stroke-width="2"/><path d="M345 180H540" stroke="#b8c3d0" stroke-dasharray="6 6"/><text x="365" y="170">x desde equilibrio</text>'
    if topic == "t4":
        return axes() + '<path d="M110 270C190 265 220 250 260 165S400 120 540 115" fill="none" stroke="#245b99" stroke-width="3"/><path d="M260 70V285" stroke="#ba513c" stroke-dasharray="7 6"/><text x="270" y="88" fill="#ba513c">cambio de régimen</text>'
    if topic == "t5" and family == "w":
        if "signo" in visual or "cruza" in visual:
            return axes() + '<path d="M110 175H585" stroke="#68788b" stroke-width="1.5"/><path d="M110 175V95H305V175H510V245H570" fill="none" stroke="#245b99" stroke-width="3"/><path d="M110 175V95H305V175Z" fill="#dceaff" opacity=".8"/><path d="M305 175H510V245H570V175Z" fill="#f7d9d3" opacity=".8"/><text x="175" y="130">área +</text><text x="405" y="225">área −</text>'
        return axes() + '<path d="M110 270L240 110L390 155L530 225" fill="none" stroke="#245b99" stroke-width="3"/><path d="M110 270L240 110L390 155L530 225V285H110Z" fill="#dceaff" opacity=".65"/><text x="350" y="315">desplazamiento</text><text x="130" y="72">fuerza</text>'
    if topic == "t5" and family == "k":
        return f'<rect x="90" y="245" width="130" height="45" fill="#dceaff" stroke="#245b99"/><rect x="410" y="145" width="130" height="145" fill="#bcefdc" stroke="#16836b"/><text x="120" y="315">estado inicial</text><text x="435" y="315">estado final</text>{arrow(230,190,390,190,"trabajo")}'
    if topic == "t5" and family == "g":
        return '<path d="M65 285C160 280 205 95 320 105S470 260 580 165" fill="none" stroke="#68788b" stroke-width="5"/><circle cx="205" cy="135" r="13" fill="#ba513c"/><circle cx="520" cy="205" r="13" fill="#245b99"/><path d="M80 135H205M80 205H520" stroke="#b8c3d0" stroke-dasharray="7 6"/><text x="90" y="125">hᵢ</text><text x="90" y="195">h_f</text>'
    if topic == "t5" and family == "e":
        return '<path d="M65 80V295" stroke="#68788b" stroke-width="8"/><path d="M65 185l30-24 30 48 30-48 30 48 30-48 30 24" fill="none" stroke="#245b99" stroke-width="3"/><rect x="255" y="140" width="105" height="90" fill="#edf4ff" stroke="#245b99"/><path d="M360 185H555" stroke="#b8c3d0" stroke-dasharray="8 6"/><text x="390" y="175">deformación x</text>'
    if topic == "t5":
        return '<rect x="70" y="245" width="95" height="55" fill="#dceaff" stroke="#245b99"/><rect x="210" y="170" width="95" height="130" fill="#bcefdc" stroke="#16836b"/><rect x="350" y="215" width="95" height="85" fill="#fff0c9" stroke="#bd7b08"/><rect x="490" y="265" width="80" height="35" fill="#f7d9d3" stroke="#ba513c"/><text x="92" y="325">K</text><text x="232" y="325">U</text><text x="366" y="325">transferencia</text><text x="500" y="325">pérdida</text>'
    if topic == "t6" and family == "i":
        return axes() + '<path d="M110 285L210 285L285 105L365 285L540 285" fill="#dceaff" stroke="#245b99" stroke-width="3"/><text x="360" y="315">tiempo</text><text x="130" y="72">fuerza</text><text x="260" y="210">impulso</text>'
    if topic == "t6" and family == "s":
        return f'<rect x="90" y="90" width="460" height="190" rx="28" fill="#f7faff" stroke="#245b99" stroke-width="2" stroke-dasharray="9 7"/><rect x="170" y="160" width="100" height="60" fill="#dceaff" stroke="#245b99"/><rect x="370" y="160" width="100" height="60" fill="#fff4e8" stroke="#ba513c"/>{arrow(270,190,350,190,"interacción","#7b5ab5")}<text x="245" y="120">frontera del sistema</text>'
    if topic == "t6" and family == "x":
        return f'<circle cx="320" cy="190" r="28" fill="#fff0c9" stroke="#bd7b08"/>{arrow(320,190,500,105,"p₁")}{arrow(320,190,145,115,"p₂","#ba513c")}{arrow(320,190,300,310,"p₃","#7b5ab5")}<text x="275" y="55">suma vectorial cerrada</text>'
    if topic == "t6" and family == "c":
        return '<path d="M55 265H585" stroke="#68788b" stroke-width="3"/><rect x="75" y="175" width="75" height="55" rx="7" fill="#dceaff" stroke="#245b99"/><rect x="165" y="175" width="75" height="55" rx="7" fill="#fff4e8" stroke="#ba513c"/><rect x="290" y="175" width="70" height="55" rx="7" fill="#dceaff" stroke="#245b99"/><rect x="350" y="175" width="70" height="55" rx="7" fill="#fff4e8" stroke="#ba513c"/><rect x="470" y="175" width="55" height="55" rx="7" fill="#dceaff" stroke="#245b99"/><rect x="530" y="175" width="55" height="55" rx="7" fill="#fff4e8" stroke="#ba513c"/><text x="112" y="295">antes</text><text x="315" y="295">interacción</text><text x="510" y="295">después</text>'
    return '<path d="M65 265H575" stroke="#68788b" stroke-width="3"/><circle cx="150" cy="215" r="24" fill="#245b99"/><circle cx="480" cy="215" r="34" fill="#ba513c"/><path d="M190 215H425" stroke="#7b5ab5" stroke-width="3" marker-end="url(#arrow)"/><text x="230" y="190">interacción por etapas</text>'


def build_all() -> tuple[dict[str, dict[str, Any]], dict[Path, str]]:
    banks: dict[str, dict[str, Any]] = {}
    assets: dict[Path, str] = {}
    for topic in TOPICS:
        rows = parse_rows(topic)
        exercises = [build_exercise(topic, row) for row in rows]
        banks[topic] = {
            "version": 1,
            "course": "1bach",
            "topic": topic,
            "topic_slug": TOPIC_META[topic]["concept"].lower().replace(" ", "-"),
            "block": TOPIC_META[topic]["concept"],
            "description": TOPIC_META[topic]["description"],
            "exercises": exercises,
        }
        for exercise, row in zip(exercises, rows):
            assets[ROOT / exercise["assets"][0]["path"]] = svg_for(exercise, row["visual"])
    return banks, assets


def validate(banks: dict[str, dict[str, Any]], assets: dict[Path, str]) -> list[str]:
    errors: list[str] = []
    all_ids: list[str] = []
    allowed = {"numeric", "single_choice", "vector", "function", "short_text", "unit_expression"}
    for topic, bank in banks.items():
        exercises = bank["exercises"]
        if len(exercises) != 60: errors.append(f"{topic}: expected 60 exercises, got {len(exercises)}")
        for exercise in exercises:
            all_ids.append(exercise["id"])
            if exercise["status"] != "draft": errors.append(f"{exercise['id']}: status must remain draft")
            if not exercise["response_fields"]: errors.append(f"{exercise['id']}: missing response fields")
            if any(field.get("type") not in allowed or not field.get("part") for field in exercise["response_fields"]): errors.append(f"{exercise['id']}: invalid response field")
            field_ids = [field.get("id") for field in exercise["response_fields"]]
            if len(field_ids) != len(set(field_ids)): errors.append(f"{exercise['id']}: duplicate response field IDs")
            for field in exercise["response_fields"]:
                if field["type"] == "single_choice":
                    option_ids = {option.get("id") for option in field.get("options", [])}
                    if field.get("correct_option_id") not in option_ids:
                        errors.append(f"{exercise['id']}.{field['id']}: invalid correct option")
                if field["type"] == "numeric" and not math.isfinite(field.get("expected_value", math.nan)):
                    errors.append(f"{exercise['id']}.{field['id']}: invalid numeric expected value")
            source = exercise["statement_source"]
            if "$" in source or "<" in source or "expected_value" in source: errors.append(f"{exercise['id']}: unsafe statement source")
            if len(exercise["assets"]) != 1: errors.append(f"{exercise['id']}: expected one diagram")
    if len(all_ids) != len(set(all_ids)): errors.append("duplicate exercise IDs")
    if len(assets) != 240: errors.append(f"expected 240 SVG assets, got {len(assets)}")
    return errors


def changed_outputs(banks: dict[str, dict[str, Any]], assets: dict[Path, str]) -> list[Path]:
    planned: dict[Path, str] = dict(assets)
    for topic, bank in banks.items():
        path = COURSE_ROOT / topic / f"exercises_{topic}.json"
        planned[path] = json.dumps(bank, ensure_ascii=False, indent=2) + "\n"
    return [path for path, content in planned.items() if not path.exists() or path.read_text(encoding="utf-8-sig") != content]


def write_outputs(banks: dict[str, dict[str, Any]], assets: dict[Path, str]) -> None:
    for topic, bank in banks.items():
        path = COURSE_ROOT / topic / f"exercises_{topic}.json"
        path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for path, content in assets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write validated JSON and SVG outputs")
    args = parser.parse_args()
    banks, assets = build_all()
    errors = validate(banks, assets)
    if errors:
        print("Validation failed:")
        for error in errors: print(f"- {error}")
        return 1
    changed = changed_outputs(banks, assets)
    print(f"Validated {sum(len(bank['exercises']) for bank in banks.values())} exercises and {len(assets)} SVGs.")
    print(f"Outputs differing from generated content: {len(changed)}")
    if args.write:
        write_outputs(banks, assets)
        print("Wrote T3-T6 JSON banks and SVG assets.")
    elif changed:
        print("Check mode only; run with --write to apply the generated outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
