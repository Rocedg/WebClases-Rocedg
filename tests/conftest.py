import os
import tempfile
from pathlib import Path

import pytest

# Flask-SQLAlchemy reads the URI when app.py initializes the extension.
TEST_DATABASE_DIR = Path(tempfile.mkdtemp(prefix="web-clases-test-db-"))
os.environ["DATABASE_URL"] = f"sqlite:///{(TEST_DATABASE_DIR / 'test.sqlite').as_posix()}"

from app import USERS, app as flask_app
from database import db
from services.account_service import ensure_seed_users


@pytest.fixture(scope="session", autouse=True)
def configure_test_database():
    flask_app.config.update(TESTING=True)
    yield


@pytest.fixture(autouse=True)
def reset_activity_database():
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        ensure_seed_users(USERS)

    yield

    with flask_app.app_context():
        db.session.remove()
