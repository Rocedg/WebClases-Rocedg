import app as app_module
from app import app as flask_app
from database import db
from models import User
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
