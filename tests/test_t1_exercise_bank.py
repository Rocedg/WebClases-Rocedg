from __future__ import annotations

import json
from pathlib import Path

from app import app as flask_app, load_exercise_catalogue
from services.exercise_presentation import exercise_number


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t1"
BLOCK_ORDER = ["r", "u", "a", "g_slopes", "g_areas", "i"]


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


def test_attempt_history_shows_the_catalogue_number():
    client = flask_app.test_client()
    client.post("/login", data={"username": "Guest", "password": "studentpass"})
    client.post("/exercise/t1_i_003/start")
    history = client.get("/practice/history")
    assert history.status_code == 200
    assert '<span class="exercise-number">59.</span>' in history.get_data(as_text=True)
