import pytest

from database import get_database_uri


@pytest.mark.parametrize(
    ("database_url", "expected"),
    [
        (
            "postgres://user:password@example.com/db",
            "postgresql+psycopg2://user:password@example.com/db",
        ),
        (
            "postgresql://user:password@example.com/db",
            "postgresql+psycopg2://user:password@example.com/db",
        ),
        (
            "postgresql+psycopg2://user:password@example.com/db",
            "postgresql+psycopg2://user:password@example.com/db",
        ),
        ("sqlite:///local.sqlite", "sqlite:///local.sqlite"),
    ],
)
def test_get_database_uri_preserves_or_selects_driver(
    monkeypatch, database_url, expected
):
    monkeypatch.setenv("DATABASE_URL", database_url)

    assert get_database_uri() == expected
