import pytest
from app.database.models import User
from app.security import hash_password

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

def _user_login(client,test_user):
    response = client.post("/login",json = {"identifier":test_user.username,"password":"test_1"})
    access_token = response.json()

    return access_token

def test_user_name_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me",headers = {"Authorization":f"Bearer {access_token}"},json={"name": "user1"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("name") == "user1"
    assert payload.get("bio") == "Test account"
    assert payload.get("work_location") == "Belagavi"
    assert payload.get("home_location") == "Jamboti"
    assert payload.get("gender") == "female"

def test_user_bio_update(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"bio":"hey there"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("bio") == "hey there"

def test_user_worklocation_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"work_location":"Bengaluru"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("work_location") == "Bengaluru"

def test_user_homelocation_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"home_location":"khanapur"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("home_location") == "khanapur"

def test_user_update_all_fields(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": "user1",
        "bio":"hey there",
        "work_location":"Bengaluru",
        "home_location":"khanapur",
        "gender": "male"
    })
    data = {
        "name": "user1",
        "bio":"hey there",
        "work_location":"Bengaluru",
        "home_location":"khanapur",
        "gender": "male"
    }
    payload = response.json()
    validate_data = {
        "name": payload.get("name"),
        "bio": payload.get("bio"),
        "work_location": payload.get("work_location"),
        "home_location": payload.get("home_location"),
        "gender": payload.get("gender")
    }

    assert response.status_code == 200
    assert validate_data == data

def test_user_with_invalid_data(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
        json = {
            "bio": None,
        })
    assert response.status_code == 422

def test_unAuthorised_user(client, test_user):
    response = client.patch("/users/me",
            json = {
                "name": "user1",
                "bio": "oye paaji tere bund phad dunga",
                "work_location":"punjab",
                "home_location":"maharastra",
                "gender": "male"
            })
    assert response.status_code == 401

def test_user_invalid_name_update(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": None,
    })

    assert response.status_code == 422

def test_user_name_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": " ",
    })

    assert response.status_code == 422

def test_user_name_with_empty_string(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": "",
    })

    assert response.status_code == 422

def test_user_worklocation_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "work_location": " ",
    })

    assert response.status_code == 422

def test_user_homelocation_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "home_location": " ",
    })

    assert response.status_code == 422

def test_user_worklocation_with_null(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "work_location": None,
    })

    assert response.status_code == 422

def test_user_homelocation_with_null(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "home_location": None,
    })

    assert response.status_code == 422

import pytest
from app.database.models import User
from app.security import hash_password

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

def _user_login(client,test_user):
    response = client.post("/login",json = {"identifier":test_user.username,"password":"test_1"})
    access_token = response.json()

    return access_token

def test_user_name_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me",headers = {"Authorization":f"Bearer {access_token}"},json={"name": "user1"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("name") == "user1"
    assert payload.get("bio") == "Test account"
    assert payload.get("work_location") == "Belagavi"
    assert payload.get("home_location") == "Jamboti"
    assert payload.get("gender") == "female"

def test_user_bio_update(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"bio":"hey there"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("bio") == "hey there"

def test_user_worklocation_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"work_location":"Bengaluru"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("work_location") == "Bengaluru"

def test_user_homelocation_update(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, json = {"home_location":"khanapur"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("home_location") == "khanapur"

def test_user_update_all_fields(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": "user1",
        "bio":"hey there",
        "work_location":"Bengaluru",
        "home_location":"khanapur",
        "gender": "male"
    })
    data = {
        "name": "user1",
        "bio":"hey there",
        "work_location":"Bengaluru",
        "home_location":"khanapur",
        "gender": "male"
    }
    payload = response.json()
    validate_data = {
        "name": payload.get("name"),
        "bio": payload.get("bio"),
        "work_location": payload.get("work_location"),
        "home_location": payload.get("home_location"),
        "gender": payload.get("gender")
    }

    assert response.status_code == 200
    assert validate_data == data

def test_user_with_invalid_data(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
        json = {
            "bio": None,
        })
    assert response.status_code == 422

def test_unAuthorised_user(client, test_user):
    response = client.patch("/users/me",
            json = {
                "name": "user1",
                "bio": "oye paaji tere bund phad dunga",
                "work_location":"punjab",
                "home_location":"maharastra",
                "gender": "male"
            })
    assert response.status_code == 401

def test_user_invalid_name_update(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": None,
    })

    assert response.status_code == 422

def test_user_name_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": " ",
    })

    assert response.status_code == 422

def test_user_name_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "name": "",
    })

    assert response.status_code == 422

def test_user_worklocation_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "work_location": " ",
    })

    assert response.status_code == 422

def test_user_homelocation_with_space(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "home_location": " ",
    })

    assert response.status_code == 422

def test_user_worklocation_with_empty_string(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "work_location": "",
    })

    assert response.status_code == 422

def test_user_homelocation_with_empty_string(client,test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me" , headers = {"Authorization": f"Bearer {access_token}"},
    json = {
        "home_location": "",
    })

    assert response.status_code == 422

def test_user_bio_with_empty_string(client, test_user):
    access_token = _user_login(client, test_user)
    response = client.patch("/users/me", headers = {"Authorization": f"Bearer {access_token}"}, 
    json = {
            "bio": ""
        })
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("bio") == ""
    