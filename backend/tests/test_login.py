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

def test_login_valid_user(client, test_user):
    
    response = client.post("/login", json = {"identifier": "test_user","password": "test_1"})
    access_token = response.json()

    assert isinstance(access_token, str)
    assert len(access_token) > 0
    assert response.status_code == 200


def test_login_invalid_password(client, test_user):
    response = client.post("/login", json = {"identifier": "test_user","password": "test_2"})
    detail = response.json()

    assert response.status_code == 401
    assert detail.get("detail") == "Unauthorized login"  

def test_login_invalid_user(client, test_user):
    response = client.post("/login", json = {"identifier": "user_1", "password":"hello@user_1"})
    detail = response.json()

    assert response.status_code == 401
    assert detail.get("detail") == "Unauthorized login"  

def test_login_empty_json(client, test_user):

    response = client.post("/login", json = {})
    
    assert response.status_code == 422

