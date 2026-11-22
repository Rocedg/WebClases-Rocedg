import json
from pathlib import Path

from app import app as flask_app


def test_app_imports_successfully():
    assert flask_app is not None
    assert flask_app.name == "app"


def test_home_returns_200():
    client = flask_app.test_client()
    response = client.get("/")

    assert response.status_code == 200


def test_login_returns_200():
    client = flask_app.test_client()
    response = client.get("/login")

    assert response.status_code == 200


def test_topics_requires_login():
    client = flask_app.test_client()
    response = client.get("/topics")

    assert response.status_code in {302, 401, 403}
    if response.status_code == 302:
        assert "/login" in response.headers["Location"]


def test_lesson_viewer_requires_login():
    client = flask_app.test_client()
    response = client.get("/lesson/T0-introduccion")

    assert response.status_code in {302, 401, 403}
    if response.status_code == 302:
        assert "/login" in response.headers["Location"]


def test_homework_requires_login():
    client = flask_app.test_client()
    response = client.get("/homework")

    assert response.status_code in {302, 401, 403}
    if response.status_code == 302:
        assert "/login" in response.headers["Location"]


def test_exams_requires_login():
    client = flask_app.test_client()
    response = client.get("/exams")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_exams_returns_200_after_login():
    client = flask_app.test_client()
    client.post(
        "/login",
        data={"username": "Guest", "password": "studentpass"},
        follow_redirects=False,
    )

    response = client.get("/exams")

    assert response.status_code == 200


def test_json_files_load_successfully():
    content_dir = Path(__file__).resolve().parents[1] / "content"

    for json_file in content_dir.rglob("*.json"):
        with json_file.open(encoding="utf-8") as file:
            assert json.load(file) is not None

    with (content_dir / "lessons" / "lessons.json").open(encoding="utf-8") as file:
        lessons = json.load(file)

    assert lessons["lessons"][0]["id"] == "T0-introduccion"
    assert Path("static/lessons/T0-introduccion.pdf").exists()


def test_main_template_rendering_does_not_crash():
    client = flask_app.test_client()

    public_paths = ["/", "/login"]
    for path in public_paths:
        response = client.get(path)
        assert response.status_code < 500

    client.post(
        "/login",
        data={"username": "Guest", "password": "studentpass"},
        follow_redirects=False,
    )

    protected_paths = ["/topics", "/lesson/T0-introduccion", "/homework", "/miscellaneous", "/exams"]
    for path in protected_paths:
        response = client.get(path)
        assert response.status_code < 500


def test_topics_page_lists_t0_lesson_after_login():
    client = flask_app.test_client()
    client.post(
        "/login",
        data={"username": "Guest", "password": "studentpass"},
        follow_redirects=False,
    )

    response = client.get("/topics")

    assert response.status_code == 200
    assert b"T0-introduccion" in response.data
    assert b"/lesson/T0-introduccion" in response.data
    assert b"/resource/lesson_pdf/T0-introduccion/download" in response.data
    assert b"/resource/lesson_pdf/T0-introduccion/open" not in response.data
    assert "Ver apunte".encode("utf-8") in response.data
