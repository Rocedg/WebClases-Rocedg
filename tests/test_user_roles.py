import app as app_module
from app import app as flask_app
from database import db
from models import User
from services.activity_service import record_activity_event
from werkzeug.security import generate_password_hash


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def set_password(username, password):
    with flask_app.app_context():
        user = db.session.scalar(db.select(User).where(User.username == username))
        user.password_hash = generate_password_hash(password)
        db.session.commit()


def test_real_accounts_log_in_with_their_roles():
    for username, password, role in [("Sandro", "fisica2027", "student"), ("Edgar", " ", "teacher")]:
        client = flask_app.test_client()
        assert login(client, username, password).status_code == 302
        with client.session_transaction() as session:
            assert session["role"] == role


def test_teacher_can_log_in_and_sees_student_pages():
    set_password("Edgar", "teacher-pass")
    client = flask_app.test_client()

    assert login(client, "Edgar", "teacher-pass").status_code == 302
    with client.session_transaction() as session:
        assert session["role"] == "teacher"
    for path in ["/topics", "/homework", "/progress", "/exams"]:
        assert client.get(path).status_code == 200
    assert "Profesor" in client.get("/topics").get_data(as_text=True)


def test_database_password_replaces_the_seed_password_for_teacher_login():
    set_password("Edgar", "database-teacher-password")
    client = flask_app.test_client()

    assert login(client, "Edgar", app_module.USERS["Edgar"][0]).status_code == 200
    assert login(client, "Edgar", "database-teacher-password").status_code == 302


def test_student_account_logs_in_as_student():
    set_password("Sandro", "student-pass")
    client = flask_app.test_client()

    assert login(client, "Sandro", "student-pass").status_code == 302
    with client.session_transaction() as session:
        assert session["role"] == "student"


def test_account_without_configured_password_cannot_log_in():
    with flask_app.app_context():
        user = db.session.scalar(db.select(User).where(User.username == "Edgar"))
        db.session.delete(user)
        db.session.commit()
    client = flask_app.test_client()

    for password in ["", "None"]:
        response = login(client, "Edgar", password)
        assert response.status_code == 200
        assert "Credenciales incorrectas" in response.get_data(as_text=True)


def test_teacher_required_only_allows_teachers():
    view = app_module.teacher_required(lambda: "panel")

    with flask_app.test_request_context():
        assert view().status_code == 302

    with flask_app.test_request_context():
        from flask import session
        session.update(username="Sandro", role="student")
        assert view()[1] == 403

    with flask_app.test_request_context():
        from flask import session
        session.update(username="Edgar", role="teacher")
        assert view() == "panel"


def test_teacher_panel_access_and_student_data():
    set_password("Edgar", "teacher-pass")
    with flask_app.app_context():
        record_activity_event(
            "Sandro",
            "lesson_viewed",
            "lesson",
            object_id="T0-introduccion",
            object_title="Apunte de Sandro",
        )
    teacher_client = flask_app.test_client()
    assert login(teacher_client, "Edgar", "teacher-pass").status_code == 302

    panel = teacher_client.get("/teacher")
    assert panel.status_code == 200
    assert "Sandro" in panel.get_data(as_text=True)

    student_page = teacher_client.get("/teacher/student/Sandro")
    assert student_page.status_code == 200
    page = student_page.get_data(as_text=True)
    assert "Sandro" in page
    assert "Apunte de Sandro" in page


def test_teacher_panel_rejects_students_and_redirects_logged_out_users():
    student_client = flask_app.test_client()
    assert login(student_client, "Sandro", "fisica2027").status_code == 302
    assert student_client.get("/teacher").status_code == 403
    assert student_client.get("/teacher/student/Sandro").status_code == 403

    anonymous_client = flask_app.test_client()
    response = anonymous_client.get("/teacher")
    assert response.status_code == 302
    assert "/login" in response.location


def test_teacher_panel_returns_404_for_unknown_student():
    set_password("Edgar", "teacher-pass")
    client = flask_app.test_client()
    assert login(client, "Edgar", "teacher-pass").status_code == 302
    assert client.get("/teacher/student/Unknown").status_code == 404
