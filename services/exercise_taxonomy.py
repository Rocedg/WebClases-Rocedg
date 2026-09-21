"""Small compatibility layer for human-readable exercise taxonomy."""

from collections import OrderedDict


TOPIC_TITLES = {
    "t0": "T0 · Herramientas para empezar Física",
    "t1": "T1 · Movimiento rectilíneo",
    "t2": "T2 · Movimiento en el plano",
    "t3": "T3 · Leyes de Newton",
    "t4": "T4 · Rozamiento y aplicaciones",
    "t5": "T5 · Energía y trabajo",
    "t6": "T6 · Momento lineal, impulso y choques",
}

LEGACY_TYPE_TITLES = {
    "units": "Unidades y análisis dimensional",
    "vectors": "Vectores y operaciones",
    "measurement": "Medida, error e incertidumbre",
    "calculus_graphs": "Cálculo y gráficas",
}


def exercise_topic_key(exercise):
    return str(exercise.get("topic") or "sin-tema")


def exercise_topic_title(exercise):
    topic = exercise_topic_key(exercise)
    return TOPIC_TITLES.get(topic, topic)


def exercise_type_title(exercise):
    """Return the pedagogical family name, never a one-letter family code."""
    explicit = exercise.get("exercise_type")
    if explicit and len(str(explicit).strip()) > 1:
        return str(explicit).strip()

    family = str(exercise.get("family") or "").strip()
    if family in LEGACY_TYPE_TITLES:
        return LEGACY_TYPE_TITLES[family]

    block = str(exercise.get("block") or "").strip()
    if block:
        return block

    return str(exercise.get("concept") or exercise_topic_title(exercise)).strip()


def exercise_type_key(exercise):
    """Stable URL/storage key; raw family values remain internal compatibility data."""
    course = str(exercise.get("course") or "course")
    topic = exercise_topic_key(exercise)
    family = str(exercise.get("family") or exercise.get("exercise_type") or "general")
    return f"{course}:{topic}:{family}"


def build_exercise_type_summaries(exercises, attempt_summaries):
    grouped = OrderedDict()
    for exercise in exercises:
        key = exercise_type_key(exercise)
        group = grouped.setdefault(
            key,
            {
                "key": key,
                "title": exercise_type_title(exercise),
                "topic": exercise_topic_key(exercise),
                "topic_title": exercise_topic_title(exercise),
                "course": exercise.get("course"),
                "count": 0,
                "difficulty_total": 0.0,
                "estimated_minutes": 0,
                "completed": 0,
                "started": 0,
            },
        )
        group["count"] += 1
        try:
            group["difficulty_total"] += float(exercise.get("difficulty") or 0)
        except (TypeError, ValueError):
            pass
        try:
            group["estimated_minutes"] += int(
                exercise.get("estimated_time_min") or exercise.get("estimated_minutes") or 0
            )
        except (TypeError, ValueError):
            pass

        status = attempt_summaries.get(str(exercise.get("id")), {}).get("status", "new")
        if status == "completed":
            group["completed"] += 1
        elif status == "started":
            group["started"] += 1

    for group in grouped.values():
        group["average_difficulty"] = round(group["difficulty_total"] / group["count"], 1)
        del group["difficulty_total"]

    return list(grouped.values())
