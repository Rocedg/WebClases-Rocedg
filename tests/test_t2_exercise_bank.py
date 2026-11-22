from __future__ import annotations

import json
from pathlib import Path

from app import app as flask_app
from services.exercise_attempt_service import GRADE_CORRECT, start_or_resume_attempt, submit_attempt
from services.exercise_bank_loader import load_topic_bank


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t2"


def statement_parts(statement: str) -> list[str]:
    return [line[1] for line in statement.splitlines() if line[:1] == "(" and line[2:3] == ")"]


def test_t2_statements_have_no_template_wording_and_parts_match_fields():
    for exercise in load_topic_bank(BANK_PATH)["exercises"]:
        statement = exercise["statement_source"]
        assert "Completa:" not in statement, exercise["id"]
        parts = statement_parts(statement)
        # Parts are consecutive letters starting at (a): no part dropped by a template.
        assert parts == [chr(ord("a") + i) for i in range(len(parts))], exercise["id"]
        assert len(parts) == exercise["parts_count"], exercise["id"]
        assert set(parts) == {field["part"] for field in exercise["response_fields"]}, exercise["id"]


def test_t2_single_choice_questions_have_distinct_real_options():
    for exercise in load_topic_bank(BANK_PATH)["exercises"]:
        for field in exercise["response_fields"]:
            if field["type"] != "single_choice":
                continue
            labels = [option["label"] for option in field["options"]]
            assert len(labels) >= 2 and len(set(labels)) == len(labels), exercise["id"]
            assert field["correct_option_id"] in {option["id"] for option in field["options"]}, exercise["id"]


def test_t2_expected_answers_grade_as_correct():
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
