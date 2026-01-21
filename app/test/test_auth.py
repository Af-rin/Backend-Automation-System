from app.models.user_model import UserModel
from app.helpers.enums.enum_config import userRoles
from app.helpers.utils.password_hash import pwd_context
from app.helpers.enums.enum_config import userRoles

API_PREFIX = "/api/v1"
AUTH_LOGIN_URL = f"{API_PREFIX}/auth/login"
AUTH_GET_USERS_URL = f"{API_PREFIX}/auth/getUsers"

def test_login_success(client, admin_user):
    payload = {
        "username": "admin",
        "email": admin_user.email,
        "password": "admin123"
    }

    response = client.post(AUTH_LOGIN_URL, json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["error"] is False
    assert "access_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    payload = {
        "username": "user1",
        "email": test_user.email,
        "password": "wrongpass"
    }

    response = client.post(AUTH_LOGIN_URL, json=payload)

    assert response.status_code == 401
    body = response.json()
    assert body["error"] is True
    assert body["data"]["message"] == "Invalid credentials."


def test_login_missing_fields(client):
    response = client.post(AUTH_LOGIN_URL, json={})
    assert response.status_code == 400
    assert response.json()["error"] is True


def admin_token(client, db):
    admin = UserModel(
        user_name="admin",
        email="admin@test.com",
        password=pwd_context.hash("admin123"),
        role=userRoles.ADMIN,
    )
    db.add(admin)
    db.commit()

    response = client.post(
        AUTH_LOGIN_URL,
        json={
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
        },
    )

    return response.json()["data"]["access_token"]


def test_get_users_success(client, db):
    # Seed users
    users = [
        UserModel(
            user_name=f"user{i}",
            email=f"user{i}@test.com",
            password="hashed",
            role=userRoles.USER,
        )
        for i in range(5)
    ]
    db.add_all(users)
    db.commit()

    token = admin_token(client, db)

    response = client.get(
        AUTH_GET_USERS_URL,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["error"] is False
    assert isinstance(body["data"]["users"], list)
    assert body["data"]["message"] == "Users fetched successfully."


def test_get_users_unauthorized(client):
    response = client.get(AUTH_GET_USERS_URL)

    assert response.status_code == 401 or response.status_code == 403


def test_get_users_with_invalid_token(client):
    response = client.get(
        AUTH_GET_USERS_URL,
        headers={"Authorization": "Bearer invalid.token.value"}
    )

    assert response.status_code == 401


def test_get_users_non_admin(client, test_user):
    response = client.post(
        AUTH_LOGIN_URL,
        json={
            "username": "user1",
            "email": test_user.email,
            "password": "correctpass",
        },
    )

    token = response.json()["data"]["access_token"]

    response = client.get(
        AUTH_GET_USERS_URL,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_get_users_pagination(client, db):
    # Seed 12 users
    users = [
        UserModel(
            user_name=f"user{i}",
            email=f"user{i}@test.com",
            password="hashed",
            role=userRoles.USER,
        )
        for i in range(12)
    ]
    
    db.add_all(users)
    db.commit()

    token = admin_token(client, db)

    response = client.get(
        f"{AUTH_GET_USERS_URL}?page=2&items_per_page=5",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()
    
    assert body["error"] is False
    assert len(body["data"]["users"]) == 5
    assert body["data"]["pagination"]["page"] == 2
    assert body["data"]["pagination"]["items_per_page"] == 5
    assert body["data"]["pagination"]["total"] == 12 + 1 # 12 users and 1 admin


def test_get_users_pagination_page_out_of_range(client, db):
    # Seed 3 users
    users = [
        UserModel(
            user_name=f"user{i}",
            email=f"user{i}@test.com",
            password="hashed",
            role=userRoles.USER,
        )
        for i in range(3)
    ]
    db.add_all(users)
    db.commit()

    token = admin_token(client, db)

    response = client.get(
        f"{AUTH_GET_USERS_URL}?page=5&limit=5",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    body = response.json()

    assert body["error"] is True
    assert body["data"]["message"] == "No users found."
