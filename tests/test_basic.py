from app import create_app

def test_app_starts():
    app = create_app()
    client = app.test_client()
    r = client.get("/login")
    assert r.status_code == 200

def test_dashboard_requires_login():
    app = create_app()
    client = app.test_client()
    r = client.get("/")
    assert r.status_code in (302, 401)

def test_login_page_exists():
    app = create_app()
    client = app.test_client()
    r = client.get("/login")
    assert r.status_code == 200