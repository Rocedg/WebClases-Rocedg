import pytest
from werkzeug.security import check_password_hash

import app as app_module
from app import app as flask_app
from database import db
from models import User
from services.account_service import (
    PASSWORD_MISMATCH,
    PASSWORD_TOO_SHORT,
    TEACHER_ACCOUNT,
    USERNAME_INVALID,
    USERNAME_TAKEN,
    create_student,
    reset_student_password,
    set_user_active,
)


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def teacher_client():
    client = flask_app.test_client()
    assert login(client, "Edgar", " ").status_code == 302
    return client


@pytest.mark.parametrize(
    ("username", "password", "repeated_password", "expected"),
    [
        ("ab", "secure-password", "secure-password", USERNAME_INVALID),
        ("a" * 31, "secure-password", "secure-password", USERNAME_INVALID),
        ("bad name", "secure-password", "secure-password", USERNAME_INVALID),
        ("alumno", "short", "short", PASSWORD_TOO_SHORT),
        ("alumno", "secure-password", "different", PASSWORD_MISMATCH),
    ],
)
def test_create_student_validates_username_and_password(
    username, password, repeated_password, expected
):
    with flask_app.app_context():
        assert create_student(username, password, repeated_password) == expected


def test_create_student_rejects_case_insensitive_duplicate_and_hashes_password():
    with flask_app.app_context():
        assert create_student("NuevoAlumno", "secure-password", "secure-password") is None
        assert create_student("nuevoalumno", "secure-password", "secure-password") == USERNAME_TAKEN
        user = db.session.scalar(db.select(User).where(User.username == "NuevoAlumno"))

        assert user is not None
        assert user.password_hash != "secure-password"
        assert check_password_hash(user.password_hash, "secure-password")
        assert user.role == app_module.ROLE_STUDENT


def test_reset_and_deactivate_refuse_teacher_accounts():
    with flask_app.app_context():
        assert reset_student_password("Edgar", "secure-password", "secure-password") == TEACHER_ACCOUNT
        assert set_user_active("Edgar", False) == TEACHER_ACCOUNT


def test_teacher_can_create_reset_deactivate_and_reactivate_student():
    client = teacher_client()

    response = client.post(
        "/teacher/accounts/create",
        data={
            "username": "CuentaNueva",
            "password": "initial-password",
            "repeated_password": "initial-password",
        },
    )
    assert response.status_code == 302
    assert "Cuenta creada" in client.get("/teacher/accounts").get_data(as_text=True)

    student_client = flask_app.test_client()
    assert login(student_client, "CuentaNueva", "initial-password").status_code == 302

    response = client.post(
        "/teacher/accounts/CuentaNueva/password",
        data={"new_password": "reset-password", "repeated_password": "reset-password"},
    )
    assert response.status_code == 302
    student_client.get("/logout")
    assert login(student_client, "CuentaNueva", "initial-password").status_code == 200
    assert login(student_client, "CuentaNueva", "reset-password").status_code == 302

    response = client.post("/teacher/accounts/CuentaNueva/active")
    assert response.status_code == 302
    student_client.get("/logout")
    assert login(student_client, "CuentaNueva", "reset-password").status_code == 200

    response = client.post("/teacher/accounts/CuentaNueva/active")
    assert response.status_code == 302
    assert login(student_client, "CuentaNueva", "reset-password").status_code == 302


@pytest.mark.parametrize(
    "path",
    [
        "/teacher/accounts",
        "/teacher/accounts/create",
        "/teacher/accounts/Sandro/password",
        "/teacher/accounts/Sandro/active",
    ],
)
def test_student_is_forbidden_from_every_teacher_accounts_route(path):
    client = flask_app.test_client()
    assert login(client, "Sandro", "fisica2027").status_code == 302
    response = client.post(path) if path != "/teacher/accounts" else client.get(path)
    assert response.status_code == 403


@pytest.mark.parametrize(
    "path",
    [
        "/teacher/accounts",
        "/teacher/accounts/create",
        "/teacher/accounts/Sandro/password",
        "/teacher/accounts/Sandro/active",
    ],
)
def test_anonymous_is_redirected_from_every_teacher_accounts_route(path):
    client = flask_app.test_client()
    response = client.post(path) if path != "/teacher/accounts" else client.get(path)
    assert response.status_code == 302
    assert "/login" in response.location
