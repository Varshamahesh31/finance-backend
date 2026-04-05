import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_rbac_viewer_creation_blocked(client):
    # Viewer tries to create user
    response = client.post(
        "/users/",
        headers={"X-User-Id": "2"},
        json={"name": "Attacker", "email": "attack@test.com"}
    )
    assert response.status_code == 403

def test_admin_create_user(client):
    # Admin successfully creating user
    response = client.post(
        "/users/",
        headers={"X-User-Id": "1"},
        json={"name": "New Guy", "email": "new.guy@test.com", "role": "analyst"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["data"]["email"] == "new.guy@test.com"

def test_create_record_and_fetch(client):
    record_payload = {
        "amount": 500.50,
        "type": "income",
        "category": "Salary",
        "date": "2026-04-10",
        "notes": "Weekly paycheck",
        "user_id": 1
    }
    
    # 1. Block Viewer from creating records
    r1 = client.post("/records/", headers={"X-User-Id": "2"}, json=record_payload)
    assert r1.status_code == 403
    
    # 2. Admin creates record securely
    r2 = client.post("/records/", headers={"X-User-Id": "1"}, json=record_payload)
    assert r2.status_code == 201
    assert r2.json()["data"]["amount"] == 500.5
    
    # 3. Viewer successfully fetches records securely (testing pagination & formatting)
    r3 = client.get("/records/", headers={"X-User-Id": "2"})
    assert r3.status_code == 200
    assert r3.json()["total"] == 1
    assert r3.json()["records"][0]["category"] == "Salary"

def test_summary_endpoints(client):
    # Validate the structure natively mapping to float outputs properly
    response = client.get("/summary/income", headers={"X-User-Id": "2"})
    assert response.status_code == 200
    assert response.json()["data"] == 500.50
    
    response = client.get("/summary/balance", headers={"X-User-Id": "2"})
    assert response.status_code == 200
    assert response.json()["data"] == 500.50

def test_date_validation_error(client):
    # Invalid date request ensuring overriding RequestValidationError yields customized structured payload
    response = client.get("/records/?start_date=bad-date", headers={"X-User-Id": "1"})
    assert response.status_code == 400
