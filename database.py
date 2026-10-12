import os
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

BASE_DIR = Path(__file__).resolve().parent
LOCAL_DATABASE_PATH = BASE_DIR / "instance" / "web_clases_rocedg.sqlite"


def get_database_uri():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    return f"sqlite:///{LOCAL_DATABASE_PATH.as_posix()}"


def init_app(app):
    LOCAL_DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", get_database_uri())
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault(
        "SQLALCHEMY_ENGINE_OPTIONS",
        {"pool_pre_ping": True, "pool_recycle": 280},
    )
    db.init_app(app)
