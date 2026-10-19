import pytest
from app.security import hash_password
from app.database.models import User

@pytest.fixture
def test_user(db_session):

    user = User(
        name = "test user",
        username="test_user",
        email="test@example.com",
        password_hash=hash_password("test_1"),
        work_location="Belagavi",
        home_location="Jamboti",
        bio="Test account",
        gender = "female"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

@pytest.fixture
def test_user2(db_session):

    user = User(
        name = "test user2",
        username="test_user2",
        email="test@example123.com",
        password_hash=hash_password("test_1"),
        work_location="Belagavi",
        home_location="Jamboti",
        bio="Test account",
        gender = "female"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def _login_test_user(client,test_user):
    response = client.post("/login",json = {"identifier":test_user.username,"password":"test_1"})
    access_token = response.json()

    return access_token

def test_add_user_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("capability") == "Software Development"

def test_delete_user_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    payload = response.json()
    response1 = client.delete(f"/users/capabilities/{payload.get("id")}", headers = {"Authorization": f"Bearer {access_token}"})
    response2 = client.get(f"/users/{test_user.id}/capabilities")
    
    capabilities= response2.json()

    assert response.status_code == 200
    assert response1.status_code == 204
    assert capabilities == []

def test_get_user_capability(client, test_user):
    access_token = _login_test_user(client, test_user)
    capabilty1 = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    capabilty1 = capabilty1.json()
    capabilty2 = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Python"})
    capabilty2 = capabilty2.json()
    capabilty3 = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"DSA"})
    capabilty3 = capabilty3.json()
    response = client.get(f"/users/{test_user.id}/capabilities")
    payload = response.json()
    capability_list = []
    for cap in payload:
        capability_list.append(cap.get("capability"))

    assert response.status_code == 200
    assert capabilty1.get("capability") in capability_list 
    assert capabilty2.get("capability") in capability_list
    assert capabilty3.get("capability") in capability_list

def test_unauthenticated_user_capability_creation(client,test_user):
    response = client.post("/users/capabilities", json = {"capability":"Python"})

    assert response.status_code == 401

def test_unauthorized_user_capability_deletion(client,test_user,test_user2):
    access_token = _login_test_user(client, test_user)
    access_token2 = _login_test_user(client, test_user2)
    response = client.post("/users/capabilities", headers ={"Authorization":f"Bearer {access_token}"} ,json = {"capability":"Python"})
    payload = response.json()
    response2 = client.delete(f"/users/capabilities/{payload.get("id")}", headers ={"Authorization":f"Bearer {access_token2}"})

    assert response2.status_code == 403

def test_empty_request(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers ={"Authorization":f"Bearer {access_token}"} ,json = {})
    assert response.status_code == 422

def test_whitespace_request(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers ={"Authorization":f"Bearer {access_token}"} ,json = {"capability":" "})
    assert response.status_code == 422

def test_empty_string_request(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers ={"Authorization":f"Bearer {access_token}"} ,json = {"capability":""})
    assert response.status_code == 422

def test_update_user_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    payload = response.json()
    patch_response = client.patch(
                f"/users/capabilities/{payload.get("id")}",
                headers = {"Authorization":f"Bearer {access_token}"},
                json = {"capability":"Python"}
    )
    updated_payload = patch_response.json()
    assert patch_response.status_code == 200
    assert updated_payload == "Python"

def test_update_user_with_empty_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    capability_response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    capability_payload = capability_response.json()
    patch_response = client.patch(
                f"/users/capabilities/{capability_payload.get("id")}",
                headers = {"Authorization":f"Bearer {access_token}"},
                json = {}
    )
    response = client.get(f"/users/{test_user.id}/capabilities")
    payload = response.json()
    capability_list = []
    for cap in payload:
        capability_list.append(cap.get("capability"))

    assert response.status_code == 200
    assert patch_response.status_code == 422
    assert capability_payload.get("capability") in capability_list

def test_update_user_with_whitespace_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    capability_response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    capability_payload = capability_response.json()
    patch_response = client.patch(
                f"/users/capabilities/{capability_payload.get("id")}",
                headers = {"Authorization":f"Bearer {access_token}"},
                json = {"capability": " "}
    )
    response = client.get(f"/users/{test_user.id}/capabilities")
    payload = response.json()
    capability_list = []
    for cap in payload:
        capability_list.append(cap.get("capability"))

    assert response.status_code == 200
    assert patch_response.status_code == 422
    assert capability_payload.get("capability") in capability_list

def test_update_user_with_empty_string_capabilty(client, test_user):
    access_token = _login_test_user(client, test_user)
    capability_response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    capability_payload = capability_response.json()
    patch_response = client.patch(
                f"/users/capabilities/{capability_payload.get("id")}",
                headers = {"Authorization":f"Bearer {access_token}"},
                json = {"capability":""}
    )
    response = client.get(f"/users/{test_user.id}/capabilities")
    payload = response.json()
    capability_list = []
    for cap in payload:
        capability_list.append(cap.get("capability"))

    assert response.status_code == 200
    assert patch_response.status_code == 422
    assert capability_payload.get("capability") in capability_list

def test_update_capability_with_Unauthorized_user(client,test_user,test_user2):
    access_token = _login_test_user(client,test_user)
    access_token2 = _login_test_user(client, test_user2)
    response = client.post("/users/capabilities", 
                                     headers = {"Authorization":f"Bearer {access_token}"},
                                     json = {"capability":"Python"})
    capability_reponse = response.json()
    response2 = client.patch(f"/users/capabilities/{capability_reponse.get("id")}",
                                      headers = {"Authorization": f"Bearer {access_token2}"},
                                     json = {"capability":"Software Developer"})

    response = client.get(f"/users/{test_user.id}/capabilities")
    payload = response.json()

    assert response.status_code == 200
    assert response2.status_code == 403
    assert payload[0].get("capability") == capability_reponse.get("capability")


def test_update_capability_with_invalid_id(client, test_user):
    access_token = _login_test_user(client, test_user)
    capability_response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    capability_payload = capability_response.json()
    patch_response = client.patch(
                "/users/capabilities/999",
                headers = {"Authorization":f"Bearer {access_token}"},
                json = {"capability":"python"})

    response = client.get(f"/users/{test_user.id}/capabilities")
    user_capabilities = response.json()

    assert capability_response.status_code == 200
    assert patch_response.status_code == 404
    assert user_capabilities[0].get("capability") == capability_payload.get("capability")

def test_delete_user_capabilty_with_invalid_id(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post("/users/capabilities", headers = {"Authorization":f"Bearer {access_token}"}, json = {"capability":"Software Development"})
    payload = response.json()
    response1 = client.delete(f"/users/capabilities/999", headers = {"Authorization": f"Bearer {access_token}"})
    response2 = client.get(f"/users/{test_user.id}/capabilities")
    capabilities = response2.json()

    assert response.status_code == 200
    assert response1.status_code == 404
    assert payload.get("capability") == capabilities[0].get("capability")