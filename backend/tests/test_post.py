import pytest
from app.database.models import User, Post
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

@pytest.fixture
def test_user2(db_session):
    

    user = User(
        name="Test User",
        username="test_user1",
        email="test@example123.com",
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

def _test_user_login(client,test_user):
    response = client.post("/login", json = {"identifier": test_user.username,"password":"test_1"})
    access_token = response.json()
    return access_token

def test_post_creation(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("caption") == "Hey i am a test user"

def test_unauthorized_user_post_creation(client):

    response = client.post("/posts",json = {"caption": "Hey i am a test user"} )
    
    assert response.status_code == 401

def test_update_post(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.patch(f"/posts/{payload.get('id')}", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption":"post edited"})
    payload1 = response1.json()

    assert response1.status_code == 200
    assert payload1.get("caption") == "post edited"
   

def test_delete_post(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.delete(f"/posts/{payload.get('id')}", headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response1.status_code == 204

def test_unauthorized_update_post(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.patch(f"/posts/{payload.get('id')}", json = {"caption":"post edited"})

    assert response1.status_code == 401

def test_unauthorized_delete_post(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.delete(f"/posts/{payload.get('id')}")
    
    assert response1.status_code == 401

def test_diffrent_user_update_post(client, test_user,test_user2):
    access_token = _test_user_login(client, test_user)
    personB = test_user2
    access_token_personB = _test_user_login(client, personB)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.patch(f"/posts/{payload.get('id')}", headers = {"Authorization": f"Bearer {access_token_personB}"}, json = {"caption":"post edited"})
    posts = client.get("/posts", params = {"limit": 2, "offset": 0})
    posts_payload = posts.json()
    
    assert posts_payload[0].get("caption") == "Hey i am a test user"
    assert response1.status_code == 403
   

def test_diffrent_user_delete_post(client, test_user, test_user2):
    access_token = _test_user_login(client, test_user)
    personB = test_user2
    access_token_personB = _test_user_login(client, personB)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.delete(f"/posts/{payload.get('id')}", headers = {"Authorization": f"Bearer {access_token_personB}"})
    
    assert response1.status_code == 403

def test_get_posts(client, test_user):
    access_token = _test_user_login(client, test_user)
    response1 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "hey damn tests takes too long"})
    post1 =  response1.json()
    response2 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "what the hell"})
    post2 = response2.json()
    response = client.get("/posts", params = {"limit": 10, "offset":0})
    payload = response.json()
    assert response.status_code == 200
    assert len(payload) == 2
    assert payload[1].get("caption") == post1.get("caption")
    assert payload[0].get("caption") == post2.get("caption")

def test_get_posts_pagination(client, test_user):
    access_token = _test_user_login(client, test_user)
    post1 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "hey damn tests takes too long"})
    post1 = post1.json()
    post2 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "what the hell"})
    post2 = post2.json()
    post3 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post3"})
    post3 = post3.json()
    post4 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post4"})
    post4 = post4.json()
    post5 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post5"})
    posts5 = post5.json()
    response = client.get("/posts", params = {"limit": 2, "offset": 1})
    payload = response.json()
    assert response.status_code == 200
    assert len(payload) == 2
    assert payload[1].get("caption") == post3.get("caption")
    assert payload[0].get("caption") == post4.get("caption")

def test_invalid_paginaton(client,test_user):
    access_token = _test_user_login(client, test_user)
    post1 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "hey damn tests takes too long"})
    post1 = post1.json()
    post2 = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "what the hell"})
    post2 = post2.json()
    post3 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post3"})
    post3 = post3.json()
    post4 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post4"})
    post4 = post4.json()
    post5 = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption": "post5"})
    posts5 = post5.json()
    response = client.get("/posts", params = {"limit": 0, "offset": 0})
    assert response.status_code == 422

def test_update_post_with_invaild_id(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.patch(f"/posts/999", headers = {"Authorization": f"Bearer {access_token}"}, json = {"caption":"post edited"})
    payload1 = response1.json()
    posts = client.get("/posts", params = {"limit": 2, "offset": 0})
    posts_payload = posts.json()
        
    assert response1.status_code == 404
    assert posts_payload[0].get("caption") == "Hey i am a test user"

def test_delete_post_with_invalid_post_id(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.delete("/posts/999", headers = {"Authorization": f"Bearer {access_token}"})
    
    posts = client.get("/posts", params = {"limit": 2, "offset": 0})
    posts_payload = posts.json()
            
    assert response1.status_code == 404
    assert posts_payload[0].get("caption") == payload.get("caption")

def test_get_empty_post_response(client, test_user):
    
    response = client.get("/posts", params = {"limit": 10, "offset":0})
    payload = response.json()

    assert response.status_code == 200
    assert payload == []

def test_get_posts_empty_json(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {})
    
    assert response.status_code == 422

def test_get_posts_empty_caption(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": ""})

    assert response.status_code == 422

def test_get_posts_with_whitespace_caption(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization":f"Bearer {access_token}"}, json = {"caption": "   "})

    assert response.status_code == 422

def test_update_post_with_null(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts", headers = {"Authorization": f"Bearer {access_token}"},json = {"caption": "Hey i am a test user"} )
    payload = response.json()
    response1 = client.patch(f"/posts/{payload.get("id")}", headers = {"Authorization": f"Bearer {access_token}"}, json = {})
    posts = client.get("/posts", params = {"limit": 2, "offset": 0})
    posts_payload = posts.json()

    assert response1.status_code == 422
    assert posts_payload[0].get("caption") == payload.get("caption")

def test_get_post(client, test_user):
    access_token = _test_user_login(client, test_user)
    response = client.post("/posts",
                            headers = {"Authorization": f"Bearer {access_token}"},
                              json={"caption": "hey this is a test post"})
    post = response.json()
    response1 = client.get(f"/posts/{post.get("id")}")
    get_post = response1.json()

    assert response.status_code == 200
    assert response1.status_code == 200
    assert get_post.get("id") == post.get("id")
    assert get_post.get("caption") == post.get("caption")

def test_get_post2(client, test_user):
    access_token = _test_user_login(client, test_user)
    response_post1 = client.post("/posts",
                            headers = {"Authorization": f"Bearer {access_token}"},
                              json={"caption": "hey this is a test post"})
    response_post2 = client.post("/posts",
                                 headers = {"Authorization": f"Bearer {access_token}"},
                                 json = {"caption":"test post 2"})
    post = response_post1.json()
    post2 = response_post2.json()
    response1 = client.get(f"/posts/{post.get("id")}")
    response2 = client.get(f"/posts/{post2.get("id")}")
    get_post = response1.json()
    get_post2 = response2.json()

    assert response_post1.status_code == 200
    assert response_post2.status_code == 200
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert get_post.get("id") == post.get("id")
    assert get_post.get("caption") == post.get("caption")
    assert get_post2.get("id") == post2.get("id")
    assert get_post2.get("caption") == post2.get("caption")

def test_get_post_with_invalid_id(client, test_user):
    access_token = _test_user_login(client,test_user)
    response_post = client.post("/posts",
                                headers = {"Authorization": f"Bearer {access_token}"},
                                json = {"caption":"test post 1"})
    post = response_post.json()
    response = client.get("/posts/2")
    response1 = client.get(f"/posts/{post.get("id")}")
    get_post = response1.json()

    assert response_post.status_code == 200
    assert response.status_code == 404
    assert response1.status_code == 200
    assert get_post.get("id") == post.get("id")
    assert get_post.get("caption") == post.get("caption")

def test_get_user_posts(client, test_user):
    access_token = _test_user_login(client, test_user)
    response_post1 = client.post("/posts",
                        headers = {"Authorization": f"Bearer {access_token}"},
                        json={"caption": "hey this is a test post"})
    response_post2 = client.post("/posts",
                        headers = {"Authorization": f"Bearer {access_token}"},
                        json = {"caption":"test post 2"})

    post1 = response_post1.json()
    post2 = response_post2.json()

    user_posts_response = client.get(f"/users/{test_user.username}/posts")
    user_post = user_posts_response.json()

    assert response_post1.status_code == 200
    assert response_post2.status_code == 200
    assert user_posts_response.status_code == 200
    assert user_post[1].get("id") == post1.get("id")
    assert user_post[1].get("caption") == post1.get("caption")
    assert user_post[0].get("id") == post2.get("id")
    assert user_post[0].get("caption") == post2.get("caption")

def test_get_user_posts_with_invalid_username(client, test_user, test_user2):
    access_token = _test_user_login(client, test_user)
    response_post1 = client.post("/posts",
                            headers = {"Authorization": f"Bearer {access_token}"},
                            json={"caption": "hey this is a test post"})
    response_post2 = client.post("/posts",
                            headers = {"Authorization": f"Bearer {access_token}"},
                            json = {"caption":"test post 2"})
    
    user_posts_response = client.get("/users/test_user3/posts")

    assert response_post1.status_code == 200
    assert response_post2.status_code == 200
    assert user_posts_response.status_code == 404

def test_get_user_post_with_no_post_user(client, test_user):
    user_posts_response = client.get(f"/users/{test_user.username}/posts")
    users_posts = user_posts_response.json()

    assert user_posts_response.status_code == 200
    assert users_posts == []