import pytest
from fastapi.testclient import TestClient

# ✅ Test V1 : Injection SQL rejetée
def test_sql_injection_rejected(client):
    response = client.get("/transactions/search", params={
        "user_id": "1' OR '1'='1",
        "keyword": "test"
    })
    assert response.status_code in [400, 422]

# ✅ Test V2 : JWT expiré rejeté
def test_expired_jwt_rejected(client):
    expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MX0.invalid"
    response = client.get("/account/123", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401

# ✅ Test V3 : IDOR - accès refusé
def test_idor_access_denied(client):
    token = create_test_token(user_id="user1")
    response = client.get("/account/compte_user2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

# ✅ Test V5 : XSS rejeté
def test_xss_sanitized(client):
    response = client.post("/transfer", json={
        "to_account": "123e4567-e89b-12d3-a456-426614174000",
        "amount": 100,
        "description": "<script>alert('XSS')</script>"
    })
    if response.status_code == 200:
        assert "<script>" not in response.json().get("description", "")

# ✅ Test V7 : Rate limiting
def test_rate_limiting(client):
    for i in range(6):
        response = client.post("/login", json={"username": "test", "password": "wrong"})
    assert response.status_code == 429
