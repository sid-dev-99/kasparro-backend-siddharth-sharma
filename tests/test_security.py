from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_missing_key():
    response = client.get("/health")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

def test_auth_invalid_key():
    response = client.get("/health", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}

def test_auth_valid_key():
    response = client.get("/health", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
