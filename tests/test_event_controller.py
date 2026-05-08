from __future__ import annotations

from fastapi.testclient import TestClient

# Como você já tem essa função no outro arquivo, 
# se ela estiver em um arquivo separado (como conftest.py) você pode importá-la.
# Caso contrário, pode defini-la aqui também para os testes de evento.
def admin_auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/users/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


# Substitua os campos abaixo pelos campos reais que existem no seu EventCreateIn
def event_payload() -> dict[str, object]:
    return {
        "description": "Um evento muito legal",
        "date": "2026-10-10T10:00:00",
        "location": "Laboratório de Informática",
    }


def test_create_event_returns_created(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    payload = event_payload()

    response = client.post("/events", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["description"] == payload["description"]
    assert data["date"] == payload["date"]
    assert data["location"] == payload["location"]


def test_list_events_returns_list_of_events(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    
    # Cria um evento primeiro para garantir que a lista não venha vazia
    client.post("/events", json=event_payload(), headers=headers)

    response = client.get("/events", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_event_by_id_returns_event(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    
    # Cria o evento
    created_event = client.post("/events", json=event_payload(), headers=headers).json()

    # Busca o evento pelo ID
    response = client.get(f"/events/{created_event['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == created_event["id"]
    assert response.json()["date"] == created_event["date"]
    assert response.json()["location"] == created_event["location"]


def test_update_event_returns_updated_event(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    
    # Cria o evento
    created_event = client.post("/events", json=event_payload(), headers=headers).json()

    # Payload para atualização (ajuste conforme o seu EventUpdateIn)
    update_payload = {
        "date": "2026-10-10T10:00:00",
        "location": "Laboratório de Informática",
    }

    # Atualiza o evento
    response = client.put(f"/events/{created_event['id']}", json=update_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == created_event["id"]
    assert response.json()["date"] == update_payload["date"]
    assert response.json()["location"] == update_payload["location"]


def test_delete_event_removes_resource(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    
    # Cria o evento
    created_event = client.post("/events", json=event_payload(), headers=headers).json()
    event_id = created_event["id"]

    # Deleta o evento
    delete_response = client.delete(f"/events/{event_id}", headers=headers)
    assert delete_response.status_code == 204

    # Tenta buscar o evento deletado e espera um 404
    get_response = client.get(f"/events/{event_id}", headers=headers)
    assert get_response.status_code == 404


def test_access_events_without_token_returns_unauthorized(client: TestClient) -> None:
    response = client.get("/events")
    assert response.status_code == 401