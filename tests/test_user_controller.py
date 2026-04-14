from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_user_returns_created_user(client: TestClient) -> None:
    response = client.post(
        "/usuarios",
        json={
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "tipo": "aluno",
        "ra": "2024001",
        "nome": "Diego",
        "senha": "segredo",
    }


def test_list_users_returns_created_users(client: TestClient) -> None:
    client.post(
        "/usuarios",
        json={
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
    )
    client.post(
        "/usuarios",
        json={
            "tipo": "professor",
            "ra": "2024002",
            "nome": "Maria",
            "senha": "senha-forte",
        },
    )

    response = client.get("/usuarios")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
        {
            "id": 2,
            "tipo": "professor",
            "ra": "2024002",
            "nome": "Maria",
            "senha": "senha-forte",
        },
    ]


def test_get_user_by_id_returns_user(client: TestClient) -> None:
    created = client.post(
        "/usuarios",
        json={
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
    ).json()

    response = client.get(f"/usuarios/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_user_uses_id_from_url_and_returns_updated_user(client: TestClient) -> None:
    created = client.post(
        "/usuarios",
        json={
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
    ).json()

    response = client.put(
        f"/usuarios/{created['id']}",
        json={
            "tipo": "professor",
            "ra": "2024999",
            "nome": "Diego Atualizado",
            "senha": "nova-senha",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "tipo": "professor",
        "ra": "2024999",
        "nome": "Diego Atualizado",
        "senha": "nova-senha",
    }


def test_delete_user_removes_resource(client: TestClient) -> None:
    created = client.post(
        "/usuarios",
        json={
            "tipo": "aluno",
            "ra": "2024001",
            "nome": "Diego",
            "senha": "segredo",
        },
    ).json()

    delete_response = client.delete(f"/usuarios/{created['id']}")
    get_response = client.get(f"/usuarios/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert get_response.json() == {
        "code": "user_not_found",
        "message": f"Usuario {created['id']} nao encontrado",
        "details": {"user_id": created["id"]},
    }


def test_create_user_with_duplicate_ra_returns_conflict_error(client: TestClient) -> None:
    payload = {
        "tipo": "aluno",
        "ra": "2024001",
        "nome": "Diego",
        "senha": "segredo",
    }

    first_response = client.post("/usuarios", json=payload)
    second_response = client.post("/usuarios", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "code": "user_ra_already_exists",
        "message": "Ja existe um usuario com este RA",
        "details": {"field": "ra", "value": "2024001"},
    }
