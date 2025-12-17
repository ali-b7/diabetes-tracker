from app import create_app

def test_app_starts():
    app = create_app()
    client = app.test_client()
    r = client.get("/login")
    assert r.status_code == 200
