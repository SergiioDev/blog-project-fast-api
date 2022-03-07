from app import schemas
from app.config import settings
from jose import jwt


def test_create_user(client):
    response = client.post("/users/",
                           json={"email": "unitTest@unit.com", "password": "unit"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "email": "unitTest@unit.com"}


def test_login(test_user,client):
    response = client.post("/login",
                           data={"username": test_user['email'], "password": test_user['password']})

    token = schemas.Token(**response.json())

    assert response.status_code == 200
    assert token.token_type == "bearer"


def test_incorrect_login(test_user, client):

    response = client.post("/login",
                           data={"username": test_user['email'], "password": "incorrect"})

    assert response.status_code == 403
