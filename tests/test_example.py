from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_endpoint():
    response = client.get("/api/public")
    assert response.status_code == 200
    assert "Hello from a public endpoint!" in response.json()["message"]

def test_login_and_private_endpoint():
    # 1. Log in
    login_response = client.post("/api/auth/token", data={"username": "user", "password": "pass"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 2. Access private endpoint
    headers = {"Authorization": f"Bearer {token}"}
    private_response = client.get("/api/private", headers=headers)
    assert private_response.status_code == 200
    assert "Hello, user. This is a private endpoint." in private_response.json()["message"]
