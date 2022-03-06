from .database import client, session
from app import schemas
from app.config import settings
from jose import jwt


def test_create_user(client):
    response = client.post("/users/",
                           json={"email": "unitTest@unit.com", "password": "unit"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "email": "unitTest@unit.com"}


def test_login(client):
    client.post("/users/",
                json={"email": "unitTest@unit.com", "password": "unit"})

    response = client.post("/login",
                           data={"username": "unitTest@unit.com", "password": "unit"})

    token = schemas.Token(**response.json())

    assert response.status_code == 200
    assert token.token_type == "bearer"
