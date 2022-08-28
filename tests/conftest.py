from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>:<port>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    """db session initiate"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    """persist unauthorized client"""

    def override_get_db():
        """call session for client object"""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """creates a user for testing"""
    user_data = {"email": "user001@gmail.com", "password": "password001"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    """creates another user for testing"""
    user_data = {"email": "user002@gmail.com", "password": "password002"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    """creates an auth token for testing"""
    return create_access_token({"user_id": test_user["users_id"]})


@pytest.fixture
def authorized_client(client, token):
    """creates client + auth token"""
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    """creates posts for us to test API"""
    # define some posts data (in dict format) for us to test
    posts_data = [
        {
            "title": "first title",
            "posts_content": "first content",
            "owner_id": test_user["users_id"],
        },
        {
            "title": "2nd title",
            "posts_content": "2nd content",
            "owner_id": test_user["users_id"],
        },
        {
            "title": "3rd title",
            "posts_content": "3rd content",
            "owner_id": test_user["users_id"],
        },
        {
            "title": "3rd title",
            "posts_content": "3rd content",
            "owner_id": test_user2["users_id"],
        },
    ]

    def create_posts_model(posts):
        # function to unpack posts_data
        return models.Post(**posts)

    # map dict to list
    posts_mapping = map(create_posts_model, posts_data)
    posts_list = list(posts_mapping)
    # add to test DB
    session.add_all(posts_list)
    session.commit()
    posted = session.query(models.Post).all()
    # result is 3 posts created in our test DB
    return posted


@pytest.fixture
def test_vote(test_user, test_posts, session):
    """commits votes on test posts"""
    new_vote = models.Votes(
        posts_id=test_posts[3].posts_id, users_id=test_user["users_id"]
    )
    session.add(new_vote)
    session.commit()
