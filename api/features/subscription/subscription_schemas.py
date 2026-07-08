from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    event_id: int
    created_at: datetime
