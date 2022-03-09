from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from .database import engine
from .database import SQLALCHEMY_DATABASE_URL
from .database import TestingSessionLocal
from app.oauth2 import create_access_token
from app import models
from alembic import command


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "unitTest@unit.com", "password": "unit"}

    response = client.post("/users/", json=user_data)

    user_data['id'] = 1
    assert response.status_code == 201
    return user_data


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_user, session):
    post_data = [
        {
            "title": "first post",
            "content": "first post content",
            "owner_id": 1
        },
        {
            "title": "second post",
            "content": "second post content",
            "owner_id": 1
        },
        {
            "title": "third post",
            "content": "third post content",
            "owner_id": 1
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()
