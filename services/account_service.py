from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models import User, utc_now


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
