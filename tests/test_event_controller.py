from __future__ import annotations

from fastapi.testclient import TestClient


def admin_auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/users/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def event_payload() -> dict[str, object]:
    return {
        "name": "Evento Legal",
        "description": "Um evento muito legal",
        "event_datetime": "2026-10-10T10:00:00",
        "event_location": "Laboratório de Informática",
    }


def test_create_event_returns_created(client: TestClient) -> None:
    headers = admin_auth_headers(client)
    payload = event_payload()

    response = client.post("/events", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["description"] == payload["description"]
    assert data["event_datetime"] == payload["event_datetime"]
    assert data["event_location"] == payload["event_location"]
    assert data["name"] == payload["name"]


def test_list_events_returns_list_of_events(client: TestClient) -> None:
    headers = admin_auth_headers(client)

    client.post("/events", json=event_payload(), headers=headers)

    response = client.get("/events", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_event_by_id_returns_event(client: TestClient) -> None:
    headers = admin_auth_headers(client)

    created_event = client.post("/events", json=event_payload(), headers=headers).json()

    response = client.get(f"/events/{created_event['id']}", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_event["id"]
    assert data["name"] == created_event["name"]
    assert data["event_datetime"] == created_event["event_datetime"]
    assert data["event_location"] == created_event["event_location"]


def test_update_event_returns_updated_event(client: TestClient) -> None:
    headers = admin_auth_headers(client)

    created_event = client.post("/events", json=event_payload(), headers=headers).json()

    update_payload = {
        "event_datetime": "2026-12-25T18:00:00",
        "name": "novo evento",
        "event_location": "Auditório Principal",
        "description": "Evento atualizado",
    }

    response = client.put(
        f"/events/{created_event['id']}",
        json=update_payload,
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_event["id"]
    assert data["name"] == update_payload["name"]
    assert data["event_datetime"].startswith(update_payload["event_datetime"])
    assert data["event_location"] == update_payload["event_location"]
    assert data["description"] == update_payload["description"]


def test_delete_event_removes_resource(client: TestClient) -> None:
    headers = admin_auth_headers(client)

    created_event = client.post("/events", json=event_payload(), headers=headers).json()
    event_id = created_event["id"]

    delete_response = client.delete(f"/events/{event_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/events/{event_id}", headers=headers)
    assert get_response.status_code == 404


def test_access_events_returns_list_of_events(client: TestClient) -> None:
    response = client.get("/events")
    assert response.status_code == 200
