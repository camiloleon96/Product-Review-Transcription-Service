from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_startup():
    """
    Test that the application starts up correctly.
    """
    response = client.get("/")
    assert response.status_code == 404


def test_routes_registered():
    """
    Test that all expected routes are registered in the app.
    """
    routes = [route.path for route in app.routes]
    assert "/api/video/transcribe" in routes
    assert "/api/video/transcription/{video_id}" in routes


def test_db_health_check():
    """
    Test the health check endpoint (if defined).
    """
    response = client.get("api/healthcheck/db")
    assert response.status_code == 200
    assert response.json() == {"db": "connected"}


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {'status': 'Healthy'}
