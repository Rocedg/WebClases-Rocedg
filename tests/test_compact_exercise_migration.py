from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from app import app as flask_app, exercise_titles_by_id, load_exercise_catalogue
from services.exercise_attempt_service import start_or_resume_attempt, submit_attempt


ROOT = Path(__file__).resolve().parents[1]
BANKS = tuple(sorted(ROOT.glob("content/exercises/1bach/t?/exercises_t?.json")))
ALLOWED_TYPES = {"numeric", "unit_expression", "single_choice", "vector", "function", "short_text"}
RETIRED = {"t0_m_007", "t0_c_007", "t0_c_018"}


def load_migration_module():
    spec = importlib.util.spec_from_file_location("migrate_compact_exercises", ROOT / "scripts/migrate_compact_exercises.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_published_t0_t1_t2_records_use_compact_safe_structured_content():
    counts = {}
    for path in BANKS:
        exercises = json.loads(path.read_text(encoding="utf-8"))["exercises"]
        counts[path.parent.name] = sum(e.get("status") != "retired" for e in exercises)
        for exercise in exercises:
            if exercise.get("status") == "retired":
                assert exercise["id"] in RETIRED
                assert exercise["retired_reason"]
                continue
            source = exercise["statement_source"] + exercise["solution_source"]
            assert "<p>" not in source and "$" not in source
            assert "statement" not in exercise and "solution" not in exercise
            assert "hints" not in exercise and "interactions" not in exercise
            assert exercise["response_fields"]
            assert all(field["type"] in ALLOWED_TYPES and field.get("part") for field in exercise["response_fields"])
            assert "Indicaciones de formato" not in source
    assert counts == {"t0": 77, "t1": 60, "t2": 60}


def test_retired_records_keep_order_ids_and_history_titles_but_are_not_published():
    catalogue_ids = {exercise["id"] for exercise in load_exercise_catalogue()["exercises"]}
    assert not (RETIRED & catalogue_ids)
    assert RETIRED.issubset(exercise_titles_by_id())
    t0_ids = [e["id"] for e in json.loads(BANKS[0].read_text(encoding="utf-8"))["exercises"]]
    assert t0_ids.index("t0_m_007") == 46
    assert t0_ids.index("t0_c_007") == 66
    assert t0_ids.index("t0_c_018") == 77


def test_migration_check_is_read_only_and_idempotent():
    module = load_migration_module()
    before = {path: path.read_bytes() for path in BANKS}
    report = module.migrate_all(write=False)
    after = {path: path.read_bytes() for path in BANKS}
    assert before == after
    assert report["retired"] == []
    assert report["migrated"] == {}


def test_function_and_short_text_fields_are_deterministically_graded():
    exercises = {e["id"]: e for e in load_exercise_catalogue()["exercises"]}
    function_exercise = exercises["t1_r_003"]
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", function_exercise)
        values = {field["id"]: "" for field in function_exercise["response_fields"]}
        values.update({"func": "3*(t-2)", "x8": "18"})
        submit_attempt("Guest", attempt.id, function_exercise, values)
        responses = {response.field_id: response for response in attempt.responses}
        assert responses["func"].grading_status == "correct"

        text_exercise = exercises["t0_v_004"]
        attempt2, _ = start_or_resume_attempt("Guest", text_exercise)
        values2 = {field["id"]: "" for field in text_exercise["response_fields"]}
        values2["quadrant"] = "ii"
        submit_attempt("Guest", attempt2.id, text_exercise, values2)
        responses2 = {response.field_id: response for response in attempt2.responses}
        assert responses2["quadrant"].grading_status == "correct"
