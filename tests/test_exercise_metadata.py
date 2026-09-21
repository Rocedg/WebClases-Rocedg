from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from app import load_exercise_catalogue


ROOT = Path(__file__).resolve().parents[1]


def load_script(relative_path: str, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_exercise_metadata_validation_allows_planned_missing_files():
    validate_exercises = load_script("scripts/validate_exercises.py", "validate_exercises")

    result = validate_exercises.validate_all(ROOT)

    assert not result.errors
    assert result.topic_file_count >= 1
    assert result.exercise_count >= 4
    assert result.warnings


def test_build_exercise_index_preview_contains_practice_fields():
    build_exercise_index = load_script("scripts/build_exercise_index.py", "build_exercise_index")

    index = build_exercise_index.build_index(ROOT, write=False)

    assert index["version"] == 1
    assert index["generated"] is True
    assert len(index["exercises"]) >= 4

    expected_ids = {
        "faraday_area_motional_001",
        "faraday_b_variable_001",
        "faraday_theta_rotation_001",
        "faraday_period_ratio_001",
    }
    assert expected_ids.issubset({exercise["id"] for exercise in index["exercises"]})

    required_fields = {
        "id",
        "version",
        "title",
        "course",
        "block",
        "topic",
        "concept",
        "exercise_type",
        "subtype",
        "difficulty",
        "estimated_time_min",
        "statement_pdf",
        "solution_pdf",
        "tags",
        "workflow",
    }
    for exercise in index["exercises"]:
        assert required_fields.issubset(exercise)
        if exercise["id"] in expected_ids:
            assert exercise["workflow"]["status"] == "planned"


def test_exercise_catalogue_loads_t0_t1_and_t2_as_separate_banks():
    exercises = load_exercise_catalogue()["exercises"]

    assert exercises
    assert all(exercise["course"] == "1bach" for exercise in exercises)
    assert "faraday_area_motional_001" not in {exercise["id"] for exercise in exercises}
    topics = {exercise["topic"] for exercise in exercises}
    assert {"t0", "t1", "t2"}.issubset(topics)
    for topic in ("t0", "t1", "t2"):
        topic_exercises = [exercise for exercise in exercises if exercise["topic"] == topic]
        assert topic_exercises
        assert all(exercise["id"].startswith(f"{topic}_") for exercise in topic_exercises)
