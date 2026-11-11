import pytest
from app.database.models import User
from app.security import hash_password

@pytest.fixture
def test_user(db_session):
    user = User(
        name = "test user",
        username = "test_user",
        email = "test@example.com",
        password_hash = hash_password("test_1"),
        work_location = "belgavi",
        home_location = "jamboti",
        gender = "male",
        bio = "test user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user2(db_session):
    user = User(
        name = "test user",
        username = "test_user2",
        email = "test@example2.com",
        password_hash = hash_password("test_1"),
        work_location = "belgavi",
        home_location = "jamboti",
        gender = "male",
        bio = "test user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user3(db_session):
    user = User(
        name = "test user",
        username = "test_user2",
        email = "test@example2.com",
        password_hash = hash_password("test_1"),
        gender = "male",
        bio = "test user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def login_test_user(client, test_user):
    response = client.post("/login", json = {"identifier":test_user.username,"password":"test_1"})
    access_token = response.json()
    return access_token

def test_create_task(client, test_user):
    access_token = login_test_user(client, test_user) 
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"}, 
                           json ={"title":"Need a developer",
                                  "description":"need a developer who can develop feelings in her for me",
                                   "location":"belgavi",
                                    "payment":"10000" })
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("title") == "Need a developer"
    assert payload.get("name") == test_user.name
    assert payload.get("username") == test_user.username

def test_create_user_with_unauthenticated_user(client):
    response = client.post("/tasks", 
                           json = {"title":"Need a developer",
                                  "description":"need a developer who can develop feelings in her for me",
                                   "location":"belgavi",
                                    "payment":"10000" } )
    payload = response.json()

    assert response.status_code == 401
    assert payload.get("detail") == "Not authenticated"

def test_create_task_with_title_as_None(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": None,
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_title_as_whitespace(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title":" ",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_title_as_empty_string(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_description_as_None(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":None,
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_description_as_whitespace(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":" ",
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_description_as_empty_string(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"",
                                "location":"belgavi",
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_location_as_None(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":None,
                                "payment":"10000" 
                           })

    assert response.status_code == 422

def test_create_task_with_location_as_whitespace(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":" ",
                                "payment":"10000" 
                           })

    assert response.status_code == 422  

def test_create_task_with_location_as_empty_string(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"",
                                "payment":"10000" 
                           })

    assert response.status_code == 422  

def test_create_task_with_payment_as_None(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":None 
                           })

    assert response.status_code == 422

def test_create_task_with_payment_as_whitespace(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":" " 
                           })

    assert response.status_code == 422

def test_create_task_with_payment_as_empty_string(client, test_user):
    access_token = login_test_user(client, test_user)
    response = client.post("/tasks", 
                           headers = {"Authorization":f"Bearer {access_token}"},
                           json = {
                                "title": "Need a developer",
                                "description":"need a developer who can develop feelings in her for me",
                                "location":"belgavi",
                                "payment":""
                           })

    assert response.status_code == 422

def test_get_task(client, test_user, test_user2):
    access_token = login_test_user(client, test_user)
    access_token2 = login_test_user(client, test_user2)
    task1_response = client.post("/tasks", 
                               headers = {"Authorization":f"Bearer {access_token2}"},
                               json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                               })
    task2_response = client.post("/tasks", 
                                   headers = {"Authorization":f"Bearer {access_token}"},
                                   json = {
                                        "title": "Need a editor",
                                        "description":"need a editor who can edit my life",
                                        "location":"belgavi",
                                        "payment":"100"
                                   })
    task3_response = client.post("/tasks", 
                                   headers = {"Authorization":f"Bearer {access_token2}"},
                                   json = {
                                        "title": "Need a developer",
                                        "description":"need a developer who can develop feelings in her for me",
                                        "location":"bengaluru",
                                        "payment":"100"
                                   })
    task4_response = client.post("/tasks", 
                                       headers = {"Authorization":f"Bearer {access_token}"},
                                       json = {
                                            "title": "Need a editor",
                                            "description":"need a editor who can edit my life",
                                            "location":"bengaluru",
                                            "payment":"100"
                                       })
    get_task_response = client.get("/tasks",
               headers = {"Authorization":f"Bearer {access_token}"},
               params = {"location":"bengaluru","limit": 5,"offset":0})
    get_task = get_task_response.json()

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert task3_response.status_code == 200
    assert task4_response.status_code == 200
    assert get_task[0].get("title") == "Need a editor"
    assert get_task[0].get("name") == test_user.name
    assert get_task[0].get("location") == "bengaluru"
    assert get_task[1].get("title") == "Need a developer"
    assert get_task[1].get("name") == test_user2.name
    assert get_task[1].get("location") == "bengaluru"

def test_get_task_with_users_location(client, test_user, test_user2):
    access_token = login_test_user(client, test_user)
    access_token2 = login_test_user(client, test_user2)
    task1_response = client.post("/tasks", 
                               headers = {"Authorization":f"Bearer {access_token2}"},
                               json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                               })
    task2_response = client.post("/tasks", 
                                   headers = {"Authorization":f"Bearer {access_token}"},
                                   json = {
                                        "title": "Need a editor",
                                        "description":"need a editor who can edit my life",
                                        "location":"belgavi",
                                        "payment":"100"
                                   })
    task3_response = client.post("/tasks", 
                                   headers = {"Authorization":f"Bearer {access_token2}"},
                                   json = {
                                        "title": "Need a developer",
                                        "description":"need a developer who can develop feelings in her for me",
                                        "location":"bengaluru",
                                        "payment":"100"
                                   })
    task4_response = client.post("/tasks", 
                                       headers = {"Authorization":f"Bearer {access_token}"},
                                       json = {
                                            "title": "Need a editor",
                                            "description":"need a editor who can edit my life",
                                            "location":"bengaluru",
                                            "payment":"100"
                                       })
    get_task_response = client.get("/tasks",
               headers = {"Authorization":f"Bearer {access_token}"},
               params = {"limit": 5,"offset":0})
    get_task = get_task_response.json()

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert task3_response.status_code == 200
    assert task4_response.status_code == 200
    assert get_task[0].get("title") == "Need a editor"
    assert get_task[0].get("name") == test_user.name
    assert get_task[0].get("location") == test_user.work_location
    assert get_task[1].get("title") == "Need a developer"
    assert get_task[1].get("name") == test_user2.name
    assert get_task[1].get("location") == test_user.work_location

def test_get_task_with_limit_1_offset_1(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": 1,"offset":1})
    get_task = get_task_response.json()
    task1 = task1_response.json()

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 200
    assert get_task[0].get("name") == test_user.name
    assert get_task[0].get("title") == task1.get("title")
    assert get_task[0].get("location") == test_user.work_location

def test_get_task_with_limit_1_offset_2(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": 1,"offset":2})
    get_task = get_task_response.json()

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 200
    assert get_task == []

def test_get_task_with_limit_10000_offset_0(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": 10000,"offset":2})
    
    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 422

def test_get_task_with_limit_minus_1_offset_0(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": -1,"offset":2})
    
    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 422

def test_get_task_with_limit_1_offset_2(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": 1,"offset": 2})
    get_task = get_task_response.json()

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 200
    assert get_task == []

def test_get_task_with_limit_10_offset_minus_1(client,test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a developer",
                                    "description":"need a developer who can develop feelings in her for me",
                                    "location":"belgavi",
                                    "payment":"100"
                                   })
    task2_response = client.post("/tasks", 
                                headers = {"Authorization":f"Bearer {access_token}"},
                                json = {
                                    "title": "Need a editor",
                                    "description":"need a editor who can edit my life",
                                    "location":"belgavi",
                                    "payment":"100"
                                    })
    get_task_response = client.get("/tasks",
                   headers = {"Authorization":f"Bearer {access_token}"},
                   params = {"limit": 10,"offset":-1
                   })
    
    assert task1_response.status_code == 200
    assert task2_response.status_code == 200
    assert get_task_response.status_code == 422

def test_update_task(client, test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks", 
                                 headers = {"Authorization":f"Bearer {access_token}"},
                                 json = {"title":"Need an editor",
                                         "description":"need an editor who can edit my life",
                                         "location":"belgavi",
                                         "payment":"100000"})
    task1 = task1_response.json()
    task1_update_response = client.patch(f"/tasks/{task1.get("id")}", 
                                     headers = {"Authorization":f"Bearer {access_token}"},
                                     json = {"title":"Need an developer",
                                             "description":"Who can develop feelings for me in her heart",
                                             "location":"bengaluru",
                                             "payment":"CEO"})
    task1_updated = task1_update_response.json()

    assert task1_response.status_code == 200 
    assert task1_update_response.status_code == 200
    assert task1_updated.get("payment") == "CEO"
    assert task1_updated.get("title") == "Need an developer"

def test_update_task_with_only_title(client, test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks",
                                headers={"Authorization":f"Bearer {access_token}"},
                                json = {"title":"test title",
                                        "description":"test description",
                                        "location":"belgavi",
                                        "payment":"100"})
    task1 = task1_response.json()
    task1_update_response =  client.patch(f"/tasks/{task1.get("id")}",
                                          headers = {"Authorization": f"Bearer {access_token}"},
                                          json = {"title":"Need a developer"})
    task1_update = task1_update_response.json()

    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 200 
    assert task1.get("description") == task1_update.get("description")
    assert task1_update.get("title") == "Need a developer"

def test_update_task_with_only_description(client, test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks",
                                headers={"Authorization":f"Bearer {access_token}"},
                                json = {"title":"test title",
                                        "description":"test description",
                                        "location":"belgavi",
                                        "payment":"100"})
    task1 = task1_response.json()
    task1_update_response =  client.patch(f"/tasks/{task1.get("id")}",
                                          headers = {"Authorization": f"Bearer {access_token}"},
                                          json = {"description":"yea boy its working"})
    task1_update = task1_update_response.json()

    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 200 
    assert task1.get("title") == task1_update.get("title")
    assert task1_update.get("description") == "yea boy its working"

def test_update_task_with_only_payment(client, test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks",
                                headers={"Authorization":f"Bearer {access_token}"},
                                json = {"title":"test title",
                                        "description":"test description",
                                        "location":"belgavi",
                                        "payment":"100"})
    task1 = task1_response.json()
    task1_update_response =  client.patch(f"/tasks/{task1.get("id")}",
                                          headers = {"Authorization": f"Bearer {access_token}"},
                                          json = {"payment":"10"})
    task1_update = task1_update_response.json()

    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 200 
    assert task1.get("description") == task1_update.get("description")
    assert task1_update.get("payment") == "10"

def test_update_task_with_only_location(client, test_user):
    access_token = login_test_user(client, test_user)
    task1_response = client.post("/tasks",
                                headers={"Authorization":f"Bearer {access_token}"},
                                json = {"title":"test title",
                                        "description":"test description",
                                        "location":"belgavi",
                                        "payment":"100"})
    task1 = task1_response.json()
    task1_update_response =  client.patch(f"/tasks/{task1.get("id")}",
                                          headers = {"Authorization": f"Bearer {access_token}"},
                                          json = {"location":"jamboti"})
    task1_update = task1_update_response.json()

    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 200 
    assert task1.get("description") == task1_update.get("description")
    assert task1_update.get("location") == "jamboti"

def test_update_task_with_none(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         headers = {"Authorization":f"Bearer {access_token}"},
                                         json = {"title": None}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 422

def test_update_task_with_whitespace(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         headers = {"Authorization":f"Bearer {access_token}"},
                                         json = {"description": " "}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 422

def test_update_task_with_empty_string(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         headers = {"Authorization":f"Bearer {access_token}"},
                                         json = {"payment": ""}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 422

def test_update_task_with_unautorized_user(client, test_user, test_user2):
    access_token =  login_test_user(client, test_user)
    access_token2 = login_test_user(client, test_user2)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         headers = {"Authorization":f"Bearer {access_token2}"},
                                         json = {"title": "test_user2"}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 403

def test_update_task_with_unauthenticated_user(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         json = {"title": "test "}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 401

def test_update_task_with_invalid_id(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })

    task1_update_response = client.patch("/tasks/2",
                                         headers = {"Authorization":f"Bearer {access_token}"},
                                         json = {"title": "test "}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 404

def test_update_task_with_empty_json(client, test_user):
    access_token =  login_test_user(client, test_user)
    task1_response =  client.post("/tasks", 
                                  headers = {"Authorization":f"Bearer {access_token}"},
                                  json = {
                                      "title":"test title",
                                      "description":"test description",
                                      "location": "belgavi",
                                      "payment": "100"
                                  })
    task1 = task1_response.json()

    task1_update_response = client.patch(f"/tasks/{task1.get("id")}",
                                         headers = {"Authorization":f"Bearer {access_token}"},
                                         json = {}) 
    
    assert task1_response.status_code == 200
    assert task1_update_response.status_code == 400

def test_get_task_with_no_location(client, test_user3):
    access_token = login_test_user(client, test_user3)
    task1_response = client.post("/tasks", 
                                 headers = {"authorization":f"Bearer {access_token}"},
                                 json = {
                                     "title":"need a devloper to fix my life",
                                     "description":"life isn't hakuna matata anymore",
                                     "payment": "10000",
                                     "location": "Belgavi"
                                 })
    get_task_response = client.get("/tasks", headers = {"authorization":f"Bearer {access_token}"})

    assert task1_response.status_code == 200
    assert get_task_response.status_code == 400