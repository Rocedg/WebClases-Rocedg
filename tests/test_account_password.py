from datetime import datetime

import app as app_module
from app import app as flask_app
from database import db
from models import ExerciseAttempt, User
from services.account_service import ensure_seed_users
from werkzeug.security import generate_password_hash


def login(client, username="Sandro", password="fisica2027"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
    )


def change_password(client, current, new, repeated=None):
    if repeated is None:
        repeated = new
    return client.post(
        "/account/password",
        data={
            "current_password": current,
            "new_password": new,
            "repeated_password": repeated,
        },
    )


def test_seeded_users_have_hashed_passwords_and_roles():
    with flask_app.app_context():
        sandro = db.session.scalar(db.select(User).where(User.username == "Sandro"))
        edgar = db.session.scalar(db.select(User).where(User.username == "Edgar"))

        assert sandro.password_hash != "fisica2027"
        assert edgar.password_hash != " "
        assert sandro.role == app_module.ROLE_STUDENT
        assert edgar.role == app_module.ROLE_TEACHER


def test_app_seed_only_creates_test_accounts_and_preserves_existing_users():
    with flask_app.app_context():
        db.session.query(User).delete()
        db.session.commit()

        ensure_seed_users(app_module.USERS)
        assert {
            user.username for user in db.session.scalars(db.select(User))
        } == {"Guest", "Edgar"}

        existing_hash = generate_password_hash("existing-password")
        db.session.add(
            User(
                username="Sandro",
                password_hash=existing_hash,
                role=app_module.ROLE_STUDENT,
                is_active=False,
            )
        )
        db.session.commit()

        ensure_seed_users(app_module.USERS)
        preserved_user = db.session.scalar(
            db.select(User).where(User.username == "Sandro")
        )

        assert preserved_user is not None
        assert preserved_user.password_hash == existing_hash
        assert preserved_user.is_active is False


def test_users_table_is_additive_to_existing_attempts():
    with flask_app.app_context():
        attempt = ExerciseAttempt(
            username="Sandro",
            exercise_id="existing-attempt",
            exercise_version=1,
        )
        db.session.add(attempt)
        db.session.commit()

        db.create_all()

        assert db.session.get(ExerciseAttempt, attempt.id) is not None
        assert db.session.scalar(
            db.select(User).where(User.username == "Sandro")
        ) is not None


def test_anonymous_account_password_requests_redirect_to_login():
    client = flask_app.test_client()

    assert client.get("/account/password").status_code == 302
    assert client.post("/account/password").status_code == 302


def test_wrong_current_password_is_rejected_first():
    client = flask_app.test_client()
    login(client)

    response = change_password(client, "incorrecta", "short", "different")

    assert "La contraseña actual no es correcta." in response.get_data(as_text=True)


def test_new_password_confirmation_must_match():
    client = flask_app.test_client()
    login(client)

    response = change_password(client, "fisica2027", "new-password", "different")

    assert "Las dos contraseñas nuevas no coinciden." in response.get_data(as_text=True)


def test_new_password_must_have_eight_characters():
    client = flask_app.test_client()
    login(client)

    response = change_password(client, "fisica2027", "short")

    assert "La nueva contraseña debe tener al menos 8 caracteres." in response.get_data(as_text=True)


def test_new_password_must_differ_from_current_password():
    client = flask_app.test_client()
    login(client)

    response = change_password(client, "fisica2027", "fisica2027")

    assert "La nueva contraseña debe ser distinta de la actual." in response.get_data(as_text=True)


def test_password_change_replaces_old_password_and_survives_seeding():
    client = flask_app.test_client()
    login(client)

    response = change_password(client, "fisica2027", "new-secure-password")

    assert response.status_code == 200
    assert "Contraseña actualizada." in response.get_data(as_text=True)
    with flask_app.app_context():
        user = db.session.scalar(db.select(User).where(User.username == "Sandro"))
        assert user.password_hash != "new-secure-password"
        assert isinstance(user.password_changed_at, datetime)
        ensure_seed_users(app_module.USERS)

    client.get("/logout")
    assert login(client, password="fisica2027").status_code == 200
    assert login(client, password="new-secure-password").status_code == 302
