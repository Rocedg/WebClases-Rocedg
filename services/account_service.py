import re

from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models import User, utc_now


USERNAME_INVALID = 'username_invalid'
USERNAME_TAKEN = 'username_taken'
PASSWORD_MISMATCH = 'password_mismatch'
PASSWORD_TOO_SHORT = 'password_too_short'
USER_NOT_FOUND = 'user_not_found'
TEACHER_ACCOUNT = 'teacher_account'


def validate_student_credentials(username, password, repeated_password):
    if not re.fullmatch(r'[A-Za-z0-9._-]{3,30}', username or ''):
        return USERNAME_INVALID
    if password != repeated_password:
        return PASSWORD_MISMATCH
    if len(password or '') < 8:
        return PASSWORD_TOO_SHORT
    return None


def create_student(username, password, repeated_password):
    error_code = validate_student_credentials(username, password, repeated_password)
    if error_code:
        return error_code

    existing_user = db.session.scalar(
        db.select(User).where(func.lower(User.username) == username.lower())
    )
    if existing_user is not None:
        return USERNAME_TAKEN

    db.session.add(
        User(
            username=username,
            password_hash=generate_password_hash(password),
            role='student',
        )
    )
    db.session.commit()
    return None


def reset_student_password(username, new_password, repeated_password):
    error_code = validate_student_credentials(username, new_password, repeated_password)
    if error_code:
        return error_code

    user = db.session.scalar(db.select(User).where(User.username == username))
    if user is None:
        return USER_NOT_FOUND
    if user.role != 'student':
        return TEACHER_ACCOUNT

    update_password(user, new_password)
    return None


def set_user_active(username, is_active):
    user = db.session.scalar(db.select(User).where(User.username == username))
    if user is None:
        return USER_NOT_FOUND
    if user.role != 'student':
        return TEACHER_ACCOUNT

    user.is_active = is_active
    db.session.commit()
    return None


def ensure_seed_users(users):
    for username, account in users.items():
        password, role = account
        if password is None:
            continue

        user = db.session.scalar(
            db.select(User).where(User.username == username)
        )
        if user is None:
            db.session.add(
                User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    role=role,
                )
            )

    db.session.commit()


def authenticate_user(username, password):
    user = db.session.scalar(
        db.select(User).where(User.username == username)
    )
    if user is None or not user.is_active:
        return None
    if not check_password_hash(user.password_hash, password):
        return None
    return user


def update_password(user, new_password):
    user.password_hash = generate_password_hash(new_password)
    user.password_changed_at = utc_now()
    db.session.commit()
