from app import app as flask_app, load_exercise_catalogue
from services.exercise_presentation import expected_answer_text


def login(username, password):
    client = flask_app.test_client()
    client.post("/login", data={"username": username, "password": password})
    return client


def test_students_cannot_open_the_solution_views():
    client = login("Guest", "studentpass")
    assert client.get("/teacher/exercises").status_code == 403
    assert client.get("/teacher/exercises/t2_h_007").status_code == 403


def test_teacher_lists_exercises_by_topic_with_numbers():
    client = login("Edgar", " ")
    page = client.get("/teacher/exercises?topic=t2")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert "/teacher/exercises/t2_v_001" in html
    assert "T2 · Movimiento en el plano" in html
    assert client.get("/teacher/exercises?topic=t9").status_code == 404
    assert "Soluciones de los ejercicios" in client.get("/teacher").get_data(as_text=True)


def test_teacher_sees_expected_answers_and_solution_without_an_attempt():
    client = login("Edgar", " ")
    html = client.get("/teacher/exercises/t2_h_007").get_data(as_text=True)
    assert "Respuestas esperadas" in html and "Solución guiada" in html
    assert "<strong>A ✓</strong>" in html
    assert "(2; -4,905) m/s" in html
    assert "/teacher/exercises/t2_h_008" in html  # next exercise
    assert client.get("/teacher/exercises/no_existe").status_code == 404


def test_every_catalogue_solution_page_renders():
    client = login("Edgar", " ")
    for exercise in load_exercise_catalogue()["exercises"]:
        assert client.get(f"/teacher/exercises/{exercise['id']}").status_code == 200, exercise["id"]


def test_expected_answer_text_formats():
    assert expected_answer_text({"type": "numeric", "expected_value": 2.019275, "unit": "s", "tolerance": 0.01}) == "2,019 s (tolerancia ±0,01)"
    assert expected_answer_text({"type": "function", "canonical_expression": "5-4*t+t^2", "variable": "t", "unit": "m"}) == "f(t) = 5-4*t+t^2 m"
    assert expected_answer_text({"type": "single_choice", "correct_option_id": "b", "options": [{"id": "a", "label": "No"}, {"id": "b", "label": "Sí"}]}) == "Sí"
