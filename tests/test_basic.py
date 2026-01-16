from app import create_app

def test_login_page_exists():
    app = create_app()
    client = app.test_client()
    r = client.get("/login")
    assert r.status_code == 200

def test_dashboard_opens_without_login():
    app = create_app()
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200

def test_history_opens_without_login():
    app = create_app()
    client = app.test_client()
    r = client.get("/history")
    assert r.status_code == 200

def test_homepage_responds(client):
    response = client.get("/")
    assert response.status_code == 200

