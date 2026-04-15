from __future__ import annotations

from pwdlib import PasswordHash

from api.features.user.user import User, UserRole
from api.features.user.user_repository import UserRepository
from api.features.user.user_schemas import UserCreateIn, UserUpdateIn
from api.shared.exceptions import ErrorCode, ResourceNotFoundError

password_hash = PasswordHash.recommended()


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create(self, payload: UserCreateIn) -> User:
        user_data = payload.model_dump(exclude={"password"})
        user = User(
            **user_data,
            password_hash=password_hash.hash(payload.password),
        )
        return await self.repository.create(user)

    async def ensure_default_admin(self) -> User | None:
        admin = await self.repository.get_first_admin()
        if admin is not None:
            return None

        user = User(
            role=UserRole.ADMIN,
            password_hash=password_hash.hash("admin123"),
            email="admin@example.com",
            name="super_user",
            is_active=True,
            ra=None,
        )
        return await self.repository.create(user)

    async def list_all(self) -> list[User]:
        return await self.repository.list_all()

    async def get_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise ResourceNotFoundError(
                f"User {user_id} not found",
                code=ErrorCode.USER_NOT_FOUND,
                details={"user_id": user_id},
            )
        return user

    async def update(self, user_id: int, payload: UserUpdateIn) -> User:
        user = await self.get_by_id(user_id)
        for field, value in payload.model_dump(exclude={"password"}).items():
            setattr(user, field, value)
        user.password_hash = password_hash.hash(payload.password)
        return await self.repository.update(user)

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.repository.delete(user)
