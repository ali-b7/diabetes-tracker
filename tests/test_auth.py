import pytest

from app import create_app
from app.models import User


@pytest.fixture()
def app():
    # Uses the test_config support we added earlier
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


def _create_user(app, email="test@example.com", password="Password123"):
    """Create a user directly in the DB (faster + deterministic for login tests)."""
    from app import db

    with app.app_context():
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


def test_register_creates_user_and_hashes_password(app, client):
    email = "newuser@example.com"
    password = "MyStrongPass123"

    r = client.post(
        "/register",
        data={"email": email, "password": password},
        follow_redirects=False,
    )

    # Your register redirects to dashboard on success
    assert r.status_code == 302

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        assert user is not None
        assert user.password_hash is not None
        assert user.password_hash != password  # ✅ hashed, not stored in plain text
        assert user.check_password(password) is True


def test_register_duplicate_email_is_blocked(app, client):
    email = "dup@example.com"
    _create_user(app, email=email, password="X")

    r = client.post(
        "/register",
        data={"email": email, "password": "AnotherPass123"},
        follow_redirects=False,
    )

    assert r.status_code == 302
    # should redirect back to register on duplicate
    assert "/register" in r.headers["Location"]

    with app.app_context():
        # still only one user with that email
        assert User.query.filter_by(email=email).count() == 1


def test_login_success_redirects_to_dashboard(app, client):
    email = "loginok@example.com"
    password = "RightPass123"
    _create_user(app, email=email, password=password)

    r = client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )

    assert r.status_code == 302
    # Your login redirects to logs.dashboard
    assert r.headers["Location"].endswith("/")


def test_login_wrong_password_redirects_back_to_login(app, client):
    email = "loginfail@example.com"
    _create_user(app, email=email, password="CorrectPass123")

    r = client.post(
        "/login",
        data={"email": email, "password": "WrongPass"},
        follow_redirects=False,
    )

    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_logout_redirects_to_dashboard(app, client):
    # Login first so logout has a session to clear
    email = "logout@example.com"
    password = "LogoutPass123"
    _create_user(app, email=email, password=password)

    r_login = client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )
    assert r_login.status_code == 302

    r_logout = client.get("/logout", follow_redirects=False)
    assert r_logout.status_code == 302
    assert r_logout.headers["Location"].endswith("/")
