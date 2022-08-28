import pytest
from jose import jwt
from app.config import settings
from app import schemas


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "hello1234@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "hello1234@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id_ = payload.get("user_id")
    assert id_ == test_user["users_id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("arot@gmail.com", "wrongpassword", 403),
        ("aortn@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("hello1234@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
