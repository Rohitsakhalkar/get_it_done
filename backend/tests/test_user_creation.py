import pytest
from app.database.models import User
from app.security import hash_password


@pytest.fixture
def test_user(db_session):
    

    user = User(
        name="Test User",
        username="test_user",
        email="test@example.com",
        password_hash=hash_password("test_1"),
        work_location="Belagavi",
        home_location="Jamboti",
        bio="Test account",
        gender = "male"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)


    return user


def test_user_creation(client):
    response = client.post("/signup", json = { 
            "name" : "Test User",
            "username" : "test_user",
            "email" : "test@example.com",
            "password" : "test_1",
            "work_location" : "Belagavi",
            "home_location" : "Jamboti",
            "bio" : "Test account",
            "gender":"male"
            } )
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("username") == "test_user"
    assert payload.get("email") == "test@example.com"

def test_user_creation_with_only_required_fields(client):
    response = client.post("/signup", json = {
        "name" : "test user",
        "username": "test_user",
        "password": "test_1",
        "email": "test@example.com"
    })
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("username") == "test_user"
    assert payload.get("work_location") is None
    assert payload.get("home_location") is None
    assert payload.get("gender") is None
    assert payload.get("bio") is None

def test_user_missing_password(client):
    response = client.post("/signup", json = {
        "name" : "test user",
        "username": "test_user",
        "email" : "test@example.com"
    })
    assert response.status_code == 422

def test_already_exist_user_registration(client, test_user):
    response = client.post("/signup", json = { 
                "name" : "Test User",
                "username" : "test_user",
                "email" : "test@example.com",
                "password" : "test_1",
                "work_location" : "Belagavi",
                "home_location" : "Jamboti",
                "bio" : "Test account",
                "gender":"male"
                } )
    assert response.status_code == 409

def test_already_exist_email(client, test_user):
    response = client.post("/signup", json = { 
                "name" : "Test User 1",
                "username" : "test_user1",
                "email" : "test@example.com",
                "password" : "test_1",
                } )
    assert response.status_code == 409

def test_already_exist_username(client, test_user):
    response = client.post("/signup", json = { 
                "name" : "Test User 1",
                "username" : "test_user",
                "email" : "test@example123.com",
                "password" : "test_1",
                } )
    assert response.status_code == 409