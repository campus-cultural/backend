from __future__ import annotations

from api.features.user.user import User
from api.features.user.user_repository import UserRepository
from api.features.user.user_schemas import UserCreateIn, UserUpdateIn
from api.shared.exceptions import ErrorCode, ResourceNotFoundError


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create(self, payload: UserCreateIn) -> User:
        user = User(**payload.model_dump())
        return await self.repository.create(user)

    async def list_all(self) -> list[User]:
        return await self.repository.list_all()

    async def get_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise ResourceNotFoundError(
                f"Usuario {user_id} nao encontrado",
                code=ErrorCode.USER_NOT_FOUND,
                details={"user_id": user_id},
            )
        return user

    async def update(self, user_id: int, payload: UserUpdateIn) -> User:
        user = await self.get_by_id(user_id)
        for field, value in payload.model_dump().items():
            setattr(user, field, value)
        return await self.repository.update(user)

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.repository.delete(user)
