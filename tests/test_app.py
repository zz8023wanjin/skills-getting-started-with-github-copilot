import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    # 测试注册
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # 先确保未注册
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # 注册
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # 重复注册应报错
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # 注销
    response3 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response3.status_code == 200
    assert f"Unregistered {email}" in response3.json()["message"]
    # 再次注销应报错
    response4 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response4.status_code == 400

def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "foo@bar.com"})
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/NonexistentActivity/unregister", params={"email": "foo@bar.com"})
    assert response.status_code == 404
