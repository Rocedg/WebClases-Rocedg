from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from app import app as flask_app, load_exercise_catalogue
from services.exercise_attempt_service import GRADE_CORRECT, start_or_resume_attempt, submit_attempt
from services.exercise_bank_loader import load_topic_bank
from services.exercise_presentation import exercise_number


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t1"
BLOCK_ORDER = ["r", "u", "a", "g_slopes", "g_areas", "i"]


def load_script(relative_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_t1_math_validator_passes():
    module = load_script("scripts/validate_t1_math.py", "validate_t1_math")
    assert module.validate_math() == []


def test_t1_numbers_run_from_1_to_60_in_catalogue_order():
    t1 = [exercise for exercise in load_exercise_catalogue()["exercises"] if exercise["topic"] == "t1"]
    assert [exercise["number"] for exercise in t1] == list(range(1, 61))
    assert [exercise_number(exercise) for exercise in t1] == list(range(1, 61))


def test_t1_blocks_go_from_easy_to_hard_and_start_at_1_or_2():
    for block in BLOCK_ORDER:
        exercises = json.loads((BANK_PATH / f"{block}.json").read_text(encoding="utf-8"))["exercises"]
        difficulties = [exercise["difficulty"] for exercise in exercises]
        assert difficulties == sorted(difficulties), block
        assert difficulties[0] <= 2, block


def test_t1_statements_have_parts_matching_fields_and_no_legacy_wording():
    for exercise in load_topic_bank(BANK_PATH)["exercises"]:
        statement = exercise["statement_source"]
        assert "Completa:" not in statement, exercise["id"]
        # Exercises say "ecuación de la posición" (or "de la velocidad"): no lesson nickname, no "ley".
        text = json.dumps(exercise, ensure_ascii=False).lower()
        assert "santo" not in text and "grial" not in text, exercise["id"]
        assert not re.search(r"\bley(es)?\b", text), exercise["id"]
        parts = {line[1] for line in statement.splitlines() if line[:1] == "(" and line[2:3] == ")"}
        assert parts == {field["part"] for field in exercise["response_fields"]}, exercise["id"]
        for field in exercise["response_fields"]:
            assert field["type"] != "short_text", exercise["id"]
            if field["type"] == "function":
                assert "**" not in field["canonical_expression"]
                assert not any(token in field["canonical_expression"] for token in (";", "<"))


def test_t1_expected_answers_grade_as_correct():
    exercises = load_topic_bank(BANK_PATH)["exercises"]

    def as_text(value):
        return str(value).replace(".", ",")

    with flask_app.app_context():
        for exercise in exercises:
            values = {}
            for field in exercise["response_fields"]:
                if field["type"] == "numeric":
                    values[field["id"]] = as_text(field["expected_value"])
                elif field["type"] == "vector":
                    values[field["id"]] = "(" + "; ".join(as_text(c) for c in field["expected_components"]) + ")"
                elif field["type"] == "single_choice":
                    values[field["id"]] = field["correct_option_id"]
                elif field["type"] == "function":
                    values[field["id"]] = field["canonical_expression"]
            attempt, _ = start_or_resume_attempt("Guest", exercise)
            submit_attempt("Guest", attempt.id, exercise, values)
            wrong = [r.field_id for r in attempt.responses if r.grading_status != GRADE_CORRECT]
            assert not wrong, (exercise["id"], wrong)


def test_attempt_history_shows_the_catalogue_number():
    client = flask_app.test_client()
    client.post("/login", data={"username": "Guest", "password": "studentpass"})
    client.post("/exercise/t1_i_003/start")
    history = client.get("/practice/history")
    assert history.status_code == 200
    assert '<span class="exercise-number">59.</span>' in history.get_data(as_text=True)
