from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient
from pwdlib import PasswordHash

from api.app import create_app
from api.features.user.user import User


def student_payload() -> dict[str, object]:
    return {
        "role": "student",
        "email": "diego@example.com",
        "name": "Diego",
        "is_active": True,
        "ra": "2024001",
        "password": "secret",
    }


def test_startup_creates_default_admin_user(client: TestClient) -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "role": "admin",
            "email": "admin@example.com",
            "name": "super_user",
            "is_active": True,
            "ra": None,
        }
    ]


def test_startup_hashes_default_admin_password(client: TestClient) -> None:
    async def get_admin_password_hash() -> str:
        async with client.app.state.database_manager.session_factory() as session:
            user = await session.get(User, 1)
            assert user is not None
            return user.password_hash

    stored_password = asyncio.run(get_admin_password_hash())

    assert stored_password != "admin123"
    assert PasswordHash.recommended().verify("admin123", stored_password)


def test_startup_does_not_duplicate_default_admin(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"

    with TestClient(create_app(database_url=database_url)) as first_client:
        first_response = first_client.get("/users")

    with TestClient(create_app(database_url=database_url)) as second_client:
        second_response = second_client.get("/users")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert len(first_response.json()) == 1
    assert second_response.json() == first_response.json()


def test_create_user_returns_created_user(client: TestClient) -> None:
    response = client.post("/users", json=student_payload())

    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "role": "student",
        "email": "diego@example.com",
        "name": "Diego",
        "is_active": True,
        "ra": "2024001",
    }


def test_create_user_hashes_password_without_exposing_it(client: TestClient) -> None:
    response = client.post("/users", json=student_payload())

    async def get_password_hash() -> str:
        async with client.app.state.database_manager.session_factory() as session:
            user = await session.get(User, response.json()["id"])
            assert user is not None
            return user.password_hash

    stored_password = asyncio.run(get_password_hash())

    assert response.status_code == 201
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
    assert stored_password != "secret"
    assert PasswordHash.recommended().verify("secret", stored_password)


def test_create_user_accepts_admin_role(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "role": "admin",
            "email": "another-admin@example.com",
            "name": "Administrador",
            "is_active": True,
            "ra": None,
            "password": "admin-secret",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "role": "admin",
        "email": "another-admin@example.com",
        "name": "Administrador",
        "is_active": True,
        "ra": None,
    }


def test_create_non_student_user_with_ra_returns_validation_error(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "role": "professor",
            "email": "maria@example.com",
            "name": "Maria",
            "is_active": True,
            "ra": "2024002",
            "password": "strong-password",
        },
    )

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"


def test_list_users_returns_created_users(client: TestClient) -> None:
    client.post("/users", json=student_payload())
    client.post(
        "/users",
        json={
            "role": "professor",
            "email": "maria@example.com",
            "name": "Maria",
            "is_active": True,
            "ra": None,
            "password": "strong-password",
        },
    )

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "role": "admin",
            "email": "admin@example.com",
            "name": "super_user",
            "is_active": True,
            "ra": None,
        },
        {
            "id": 2,
            "role": "student",
            "email": "diego@example.com",
            "name": "Diego",
            "is_active": True,
            "ra": "2024001",
        },
        {
            "id": 3,
            "role": "professor",
            "email": "maria@example.com",
            "name": "Maria",
            "is_active": True,
            "ra": None,
        },
    ]


def test_get_user_by_id_returns_user(client: TestClient) -> None:
    created = client.post("/users", json=student_payload()).json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_user_uses_id_from_url_and_returns_updated_user(client: TestClient) -> None:
    created = client.post("/users", json=student_payload()).json()

    response = client.put(
        f"/users/{created['id']}",
        json={
            "role": "professor",
            "email": "diego.updated@example.com",
            "name": "Diego Atualizado",
            "is_active": False,
            "ra": None,
            "password": "new-password",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "role": "professor",
        "email": "diego.updated@example.com",
        "name": "Diego Atualizado",
        "is_active": False,
        "ra": None,
    }


def test_delete_user_removes_resource(client: TestClient) -> None:
    created = client.post("/users", json=student_payload()).json()

    delete_response = client.delete(f"/users/{created['id']}")
    get_response = client.get(f"/users/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert get_response.json() == {
        "code": "user_not_found",
        "message": f"User {created['id']} not found",
        "details": {"user_id": created["id"]},
    }


def test_create_user_with_duplicate_ra_returns_conflict_error(client: TestClient) -> None:
    payload = student_payload()

    first_response = client.post("/users", json=payload)
    second_response = client.post("/users", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "code": "user_ra_already_exists",
        "message": "A user with this RA already exists",
        "details": {"field": "ra", "value": "2024001"},
    }
