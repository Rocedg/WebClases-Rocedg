from app import load_exercise_catalogue
from services.exercise_presentation import exercise_number

TOPICS = ["t0", "t1", "t2", "t3", "t4", "t5", "t6"]


def test_every_first_year_topic_is_numbered_from_1_in_catalogue_order():
    exercises = [e for e in load_exercise_catalogue()["exercises"] if e.get("course") == "1bach"]
    for topic in TOPICS:
        visible = [e for e in exercises if e["topic"] == topic and e.get("status") != "retired"]
        assert visible, topic
        expected = list(range(1, len(visible) + 1))
        assert [e.get("number") for e in visible] == expected, topic
        assert [exercise_number(e) for e in visible] == expected, topic
