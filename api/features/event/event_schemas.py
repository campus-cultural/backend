from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventBaseSchema(BaseModel):
    user_id: int
    image: bytes | None = None
    event_datetime: datetime
    event_location: str
    description: str


class EventCreateIn(EventBaseSchema):
    pass


class EventCreateOut(EventBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class EventReadOut(EventBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class EventUpdateIn(BaseModel):
    image: bytes | None = None
    event_datetime: datetime | None = None
    event_location: str | None = None
    description: str | None = None


class EventUpdateOut(EventBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
