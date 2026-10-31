from jose import jwt
from app.main import app

from app import schemas

import pytest
import os
from dotenv import load_dotenv

def test_root(client):
    res = client.get("/")
    print(res)
    print(res.json().get('status'))
    assert res.json().get('status') =="success"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", 
        json={"email": "AB@gmail.com", "password": "12345678"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "AB@gmail.com"
    assert res.status_code == 201 

def test_login_user(client, test_user):
    res = client.post(
        "/login", 
        data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )
    assert res.status_code == status_code