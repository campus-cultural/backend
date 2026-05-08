from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from api.features.event.event_schemas import (
    EventCreateIn,
    EventCreateOut,
    EventReadOut,
    EventUpdateIn,
    EventUpdateOut,
)
from api.features.event.event_service import EventService
from api.features.user.user import User
from api.shared.dependencies import get_current_user, get_event_service

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventCreateOut, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreateIn,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventCreateOut:
    event = await service.create(payload, current_user)
    return EventCreateOut.model_validate(event)


@router.get("", response_model=list[EventReadOut])
async def list_events(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> list[EventReadOut]:
    events = await service.list_by_user_id(current_user.id)
    return [EventReadOut.model_validate(event) for event in events]


@router.get("/{event_id}", response_model=EventReadOut)
async def get_event(
    event_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventReadOut:
    event = await service.get_by_id(event_id)
    return EventReadOut.model_validate(event)


@router.put("/{event_id}", response_model=EventUpdateOut)
async def update_event(
    event_id: int,
    payload: EventUpdateIn,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventUpdateOut:
    event = await service.update(event_id, payload, current_user)
    return EventUpdateOut.model_validate(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> Response:
    await service.delete(event_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
