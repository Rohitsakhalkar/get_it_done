import pytest
from app.database.models import User
from app.security import hash_password

@pytest.fixture
def test_user(db_session):

    user = User(
        name = "test user",
        username = "test_user1",
        email = "test@example.com",
        password_hash = hash_password("test_1"),
        work_location ="Belagavi",
        home_location ="Jamboti",
        bio = "Test account",
        gender = "male"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

@pytest.fixture
def test_user2(db_session):

    user = User(
        name = "test user2",
        username = "test_user2",
        email = "test@example2.com",
        password_hash = hash_password("test_1"),
        work_location ="Belagavi",
        home_location ="Jamboti",
        bio = "Test account",
        gender = "male"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

@pytest.fixture
def test_user3(db_session):

    user = User(
        name = "test user3",
        username = "test_user3",
        email = "test@example3.com",
        password_hash = hash_password("test_1"),
        work_location ="Belagavi",
        home_location ="Jamboti",
        bio = "Test account",
        gender = "male"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def _login_test_user(client,test_user):
    access_token = client.post("/login", 
                    json ={"identifier":test_user.username, 
                    "password":"test_1"})
    return access_token.json()

def test_follow_a_user(client, test_user,test_user2):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("followed_by") == test_user.id
    assert payload.get("followed_to") == test_user2.id
    assert payload.get("followed_by_username") == test_user.username
    assert payload.get("followed_to_username") == test_user2.username

def test_follow_with_unauthorized_user(client, test_user):
    response = client.post(f"/users/{test_user.username}/follow")

    assert response.status_code == 401

def test_follow_user_that_does_not_exist(client, test_user):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/test_user4/follow",headers = {"Authorization":f"Bearer {access_token}"})

    assert response.status_code == 404

def test_unfollow_user(client, test_user,test_user2):
    access_token = _login_test_user(client, test_user)
    follow_reponse = client.post(f"/users/{test_user2.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    unfollow_response = client.delete(f"/users/{test_user2.username}/follow", headers={"Authorization":f"Bearer {access_token}"})

    assert follow_reponse.status_code == 200
    assert unfollow_response.status_code == 204

def test_unfollow_a_user_two_times(client, test_user,test_user2):
    access_token = _login_test_user(client, test_user)
    follow_reponse = client.post(f"/users/{test_user2.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    unfollow_response = client.delete(f"/users/{test_user2.username}/follow", headers={"Authorization":f"Bearer {access_token}"})
    unfollow_response2 = client.delete(f"/users/{test_user2.username}/follow", headers={"Authorization":f"Bearer {access_token}"})

    assert follow_reponse.status_code == 200
    assert unfollow_response.status_code == 204
    assert unfollow_response2.status_code == 404

def test_unauthorized_unfollow(client, test_user,test_user2):
    access_token = _login_test_user(client,test_user)
    response = client.post(f"/users/{test_user2.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})

    unfollow_response = client.delete(f"/users/{test_user2.username}/follow")

    assert response.status_code == 200
    assert unfollow_response.status_code == 401

def test_unfollow_with_nonexistent_username(client,test_user,test_user2):
    access_token = _login_test_user(client,test_user)
    response = client.post(f"/users/{test_user2.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    unfollow_response = client.delete("/users/TestUser2/follow",headers = {"Authorization":f"Bearer {access_token}"})

    assert response.status_code == 200
    assert unfollow_response.status_code == 404

def test_get_followers_count(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    follower_count_response = client.get(f"/users/{test_user.username}/followers/count")
    follower_count = follower_count_response.json()
    
    assert response.status_code == 200
    assert response2.status_code == 200
    assert follower_count_response.status_code == 200
    assert follower_count == 2

def test_following_count(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_count_response = client.get(f"/users/{test_user.username}/followings/count")
    following_count = following_count_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_count_response.status_code == 200
    assert following_count == 2

def test_get_followers_count_with_a_unfollow(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    unfollow_response = client.delete(f"/users/{test_user.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    follower_count_response = client.get(f"/users/{test_user.username}/followers/count")
    follower_count = follower_count_response.json()
    
    assert response.status_code == 200
    assert response2.status_code == 200
    assert unfollow_response.status_code == 204
    assert follower_count_response.status_code == 200
    assert follower_count == 1

def test_following_count_with_a_unfollow(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    unfollow_response = client.delete(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_count_response = client.get(f"/users/{test_user.username}/followings/count")
    following_count = following_count_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert unfollow_response.status_code == 204
    assert following_count_response.status_code == 200
    assert following_count == 1

def test_get_followers(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":10,"offset": 0})
    get_followers = get_follower_response.json() 

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 200
    assert get_followers[0].get("follower_username") == test_user2.username
    assert get_followers[1].get("follower_username") == test_user3.username

def test_followings(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 10,"offset": 0})
    followings = following_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 200
    assert followings[0].get("following_username") == test_user2.username
    assert followings[1].get("following_username") == test_user3.username


def test_get_followers_with_limit_1(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":1,"offset": 0})
    get_followers = get_follower_response.json() 

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 200
    assert get_followers[0].get("follower_username") == test_user2.username
    

def test_followings_with_limit_1(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 1,"offset": 0})
    followings = following_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 200
    assert followings[0].get("following_username") == test_user2.username


def test_get_followers_with_limit_1_offset_1(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":1,"offset": 1})
    get_followers = get_follower_response.json() 

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 200
    assert get_followers[0].get("follower_username") == test_user3.username

def test_followings_with_limit_1_offset_1(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 1,"offset": 1})
    followings = following_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 200
    assert followings[0].get("following_username") == test_user3.username


def test_get_followers_with_limit_2_offset_2(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":2,"offset": 2})
    get_followers = get_follower_response.json() 

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 200
    assert get_followers == []

def test_followings_with_limit_2_offset_2(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 2,"offset": 2})
    followings = following_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 200
    assert followings == []

def test_get_followers_with_no_followers(client,test_user):
    follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit": 10,"offset": 0})
    follower = follower_response.json()

    assert follower_response.status_code == 200
    assert follower == []

def test_get_followings_with_no_followings(client,test_user):
    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 10,"offset": 0})
    followings = following_response.json()

    assert following_response.status_code == 200
    assert followings == []

def test_get_followers_with_limit_2_offset_3(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":2,"offset": 3})
    get_followers = get_follower_response.json() 

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 200
    assert get_followers == []

def test_followings_with_limit_2_offset_3(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 2,"offset": 3})
    followings = following_response.json()

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 200
    assert followings == []

def test_get_followers_with_limit_0_offset_0(client, test_user,test_user2, test_user3):
    access_token = _login_test_user(client, test_user2)
    access_token2 = _login_test_user(client,test_user3)
    response = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user.username}/follow", headers = {"Authorization":f"Bearer {access_token2}"})

    get_follower_response = client.get(f"/users/{test_user.username}/followers",params = {"limit":0,"offset": 0})
     

    assert response.status_code == 200
    assert response2.status_code == 200
    assert get_follower_response.status_code == 422


def test_followings_with_limit_0_offset_0(client, test_user, test_user2,test_user3):
    access_token = _login_test_user(client, test_user)
    response = client.post(f"/users/{test_user2.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})
    response2 = client.post(f"/users/{test_user3.username}/follow",headers = {"Authorization":f"Bearer {access_token}"})

    following_response = client.get(f"/users/{test_user.username}/followings",params = {"limit": 0,"offset": 0})

    assert response.status_code == 200
    assert response2.status_code == 200
    assert following_response.status_code == 422
