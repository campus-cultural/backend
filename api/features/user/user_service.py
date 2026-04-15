from __future__ import annotations

from pwdlib import PasswordHash

from api.features.user.user import User, UserRole
from api.features.user.user_repository import UserRepository
from api.features.user.user_schemas import TokenOut, UserCreateIn, UserLoginIn, UserUpdateIn
from api.shared.exceptions import ErrorCode, ResourceNotFoundError, UnauthorizedError
from api.shared.security import create_access_token

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

    async def login(self, payload: UserLoginIn) -> TokenOut:
        user = await self.repository.get_by_email(payload.email)
        if user is None or not password_hash.verify(payload.password, user.password_hash):
            raise UnauthorizedError(
                "Invalid email or password",
                code=ErrorCode.INVALID_CREDENTIALS,
            )
        if not user.is_active:
            raise UnauthorizedError(
                "Inactive user",
                code=ErrorCode.INVALID_CREDENTIALS,
            )
        return self.create_token(user)

    def create_token(self, user: User) -> TokenOut:
        return TokenOut(access_token=create_access_token(user))

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

    async def update_profile_picture(self, user_id: int, profile_picture: bytes) -> User:
        user = await self.get_by_id(user_id)
        user.profile_picture = profile_picture
        return await self.repository.update(user)

    async def get_profile_picture(self, user_id: int) -> bytes:
        user = await self.get_by_id(user_id)
        if user.profile_picture is None:
            raise ResourceNotFoundError(
                f"User {user_id} profile picture not found",
                code=ErrorCode.USER_PROFILE_PICTURE_NOT_FOUND,
                details={"user_id": user_id},
            )
        return user.profile_picture

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.repository.delete(user)
