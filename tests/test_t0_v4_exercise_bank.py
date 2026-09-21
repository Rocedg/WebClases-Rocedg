from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from app import app as flask_app
from database import db
from models import ExerciseAttempt
from services.exercise_attempt_service import (
    GRADE_CORRECT,
    GRADE_INCORRECT,
    GRADE_PENDING_REVIEW,
    normalize_response,
    start_or_resume_attempt,
    submit_attempt,
)


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t0" / "exercises_t0.json"


def load_script(relative_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_t0_bank():
    with BANK_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def login(client, username="Guest"):
    password = "studentpass" if username == "Guest" else "fisica2026"
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=False)


def test_t0_v4_catalogue_validator_passes():
    validator = load_script("scripts/validate_t0_v4_bank.py", "validate_t0_v4_bank_test")

    assert validator.validate_bank(ROOT) == []


def test_t0_v4_math_validator_passes():
    validator = load_script("scripts/validate_t0_v4_math.py", "validate_t0_v4_math_test")

    assert validator.validate_math() == []


def test_t0_v4_active_distribution_and_retired_ids():
    bank = load_t0_bank()
    exercises = bank["exercises"]
    ids = {exercise["id"] for exercise in exercises}

    assert len(exercises) == 80
    assert len(ids) == 80
    assert sum(1 for exercise in exercises if exercise["family"] == "units") == 16
    assert sum(1 for exercise in exercises if exercise["family"] == "vectors") == 24
    assert sum(1 for exercise in exercises if exercise["family"] == "measurement") == 20
    assert sum(1 for exercise in exercises if exercise["family"] == "calculus_graphs") == 20
    assert {exercise["version"] for exercise in exercises} == {4}
    assert all(exercise["difficulty"] != 1 for exercise in exercises)
    assert not (ids & set(bank["retired_ids"]))


def test_t0_v4_required_svg_assets_exist_and_are_accessible():
    bank = load_t0_bank()
    mandatory_ids = {"t0_v_012", "t0_v_017", "t0_v_018", "t0_v_024", "t0_c_016", "t0_c_019", "t0_c_020"}

    for exercise in bank["exercises"]:
        if exercise["id"] not in mandatory_ids:
            continue
        assert exercise["assets"]
        for asset in exercise["assets"]:
            svg_path = ROOT / asset["path"]
            svg = svg_path.read_text(encoding="utf-8")
            assert "viewBox=" in svg
            assert "<title" in svg
            assert "<desc" in svg


def test_t0_v4_numeric_exact_forms_units_and_pending_review():
    bank = load_t0_bank()
    c020 = next(exercise for exercise in bank["exercises"] if exercise["id"] == "t0_c_020")
    unit_exercise = next(exercise for exercise in bank["exercises"] if exercise["id"] == "t0_u_001")

    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", c020)
        submit_attempt(
            "Guest",
            attempt.id,
            c020,
            {
                "zero_time": "36/7",
                "positive_area": "14,286",
                "negative_signed": "-1,286",
                "displacement": "13,0",
                "distance": "109/7",
            },
        )
        responses = {response.field_id: response for response in attempt.responses}
        assert responses["zero_time"].grading_status == GRADE_CORRECT
        assert responses["distance"].grading_status == GRADE_CORRECT

        attempt2, _ = start_or_resume_attempt("Guest", unit_exercise)
        submit_attempt(
            "Guest",
            attempt2.id,
            unit_exercise,
            {"distance_m": "12600", "time_s": "1080", "speed": "11,7", "dimension": "L T^-1"},
        )
        responses2 = {response.field_id: response for response in attempt2.responses}
        assert responses2["dimension"].grading_status == GRADE_CORRECT
        assert normalize_response("", "unit_expression") == ""

        mixed = {
            "id": "mixed_open_t0_test",
            "version": 4,
            "title": "Mixed",
            "interactions": [{"id": "reason", "type": "open_text", "required": True}],
        }
        attempt3, _ = start_or_resume_attempt("Guest", mixed)
        submit_attempt("Guest", attempt3.id, mixed, {"reason": "Explico el eje."})
        assert attempt3.responses[0].grading_status == GRADE_PENDING_REVIEW


def test_t0_gravitational_constant_units_regression_grades_three_of_three():
    bank = load_t0_bank()
    exercise = next(item for item in bank["exercises"] if item["id"] == "t0_u_009")

    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", exercise)
        submit_attempt(
            "Guest",
            attempt.id,
            exercise,
            {
                "unit_derived": "N*m^2/kg^2",
                "unit_base": "m^3/(kg*s^2)",
                "force_factor": "4/9",
            },
        )
        responses = {response.field_id: response for response in attempt.responses}
        assert responses["unit_derived"].raw_value == "N*m^2/kg^2"
        assert responses["unit_base"].raw_value == "m^3/(kg*s^2)"
        assert responses["unit_derived"].grading_status == GRADE_CORRECT
        assert responses["unit_base"].grading_status == GRADE_CORRECT
        assert responses["force_factor"].grading_status == GRADE_CORRECT
        assert attempt.score == 3
        assert attempt.max_score == 3


def test_t0_v4_empty_required_numeric_is_not_correct():
    bank = load_t0_bank()
    exercise = next(item for item in bank["exercises"] if item["id"] == "t0_u_001")

    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", exercise)
        submit_attempt(attempt.username, attempt.id, exercise, {"distance_m": "", "time_s": "", "speed": "", "dimension": ""})
        responses = {response.field_id: response for response in attempt.responses}
        assert responses["distance_m"].grading_status == GRADE_INCORRECT
        assert responses["dimension"].grading_status == GRADE_INCORRECT


def test_retired_t0_attempt_history_does_not_link_to_missing_exercise():
    with flask_app.app_context():
        db.session.add(
            ExerciseAttempt(
                username="Guest",
                exercise_id="t0_u_017",
                exercise_version=3,
                status="submitted",
            )
        )
        db.session.commit()

    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/practice/history")

    assert response.status_code == 200
    assert b"t0_u_017" in response.data
    assert b"Ejercicio retirado del cat" in response.data
    assert b"/exercise/t0_u_017/attempt/" not in response.data
