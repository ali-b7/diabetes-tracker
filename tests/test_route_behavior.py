import pytest

from app import create_app
from app.models import GlucoseLog, InsulinLog

pytestmark = pytest.mark.integration


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
        }
    )
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_glucose_post_saves_row_and_redirects(app, client):
    r = client.post(
        "/log/glucose",
        data={
            "value": "120",
            "unit": "mg/dL",
            "notes": "after lunch",
            "recorded_at": "",
        },
    )
    assert r.status_code == 302
    assert r.headers["Location"].endswith("/")

    with app.app_context():
        row = GlucoseLog.query.one()
        assert row.value == 120.0
        assert row.unit == "mg/dL"
        assert row.notes == "after lunch"


def test_glucose_post_invalid_value_does_not_save(app, client):
    r = client.post("/log/glucose", data={"value": "abc", "unit": "mg/dL"})
    assert r.status_code == 302
    assert "/log/glucose" in r.headers["Location"]

    with app.app_context():
        assert GlucoseLog.query.count() == 0


def test_insulin_post_requires_type(app, client):
    r = client.post(
        "/log/insulin",
        data={
            "insulin_type": "",
            "units": "5",
            "notes": "forgot type",
            "recorded_at": "",
        },
    )
    assert r.status_code == 302
    assert "/log/insulin" in r.headers["Location"]

    with app.app_context():
        assert InsulinLog.query.count() == 0


def test_insulin_post_saves_row_and_redirects(app, client):
    r = client.post(
        "/log/insulin",
        data={
            "insulin_type": "Rapid",
            "units": "6",
            "notes": "before dinner",
            "recorded_at": "",
        },
    )
    assert r.status_code == 302
    assert r.headers["Location"].endswith("/")

    with app.app_context():
        row = InsulinLog.query.one()
        assert row.insulin_type == "Rapid"
        assert row.units == 6.0
        assert row.notes == "before dinner"
