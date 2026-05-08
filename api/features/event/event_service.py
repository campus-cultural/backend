from api.features.event.event import Event
from api.features.event.event_repository import EventRepository
from api.features.event.event_schemas import EventCreateIn, EventUpdateIn
from api.features.user.user import User
from api.shared.exceptions import ErrorCode, ResourceNotFoundError


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def create(self, payload: EventCreateIn, user: User) -> Event:
        event_data = payload.model_dump()

        # vínculo com usuário
        event_data["user_id"] = user.id

        event = Event(**event_data)

        return await self.repository.create(event)

    async def list_all(self) -> list[Event]:
        return await self.repository.list_all()

    async def get_by_id(self, event_id: int) -> Event:
        event = await self.repository.get_by_id(event_id)
        if event is None:
            raise ResourceNotFoundError(
                f"Event {event_id} not found",
                code=ErrorCode.EVENT_NOT_FOUND,
                details={"event_id": event_id},
            )
        return event

    async def list_by_user_id(self, user_id: int) -> list[Event]:
        return await self.repository.get_by_user_id(user_id)

    async def update(
        self,
        event_id: int,
        payload: EventUpdateIn,
        user: User,
    ) -> Event:
        event = await self.get_by_id(event_id)

        #  proteção: só dono pode alterar
        if event.user_id != user.id:
            raise ResourceNotFoundError(
                "Event not found",
                code=ErrorCode.EVENT_NOT_FOUND,
            )

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        return await self.repository.update(event)

    async def delete(self, event_id: int, user: User) -> None:
        event = await self.get_by_id(event_id)

        #  proteção: só dono pode deletar
        if event.user_id != user.id:
            raise ResourceNotFoundError(
                "Event not found",
                code=ErrorCode.EVENT_NOT_FOUND,
            )

        await self.repository.delete(event)
