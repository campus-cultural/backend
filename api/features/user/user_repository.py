from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.features.user.user import User
from api.shared.exceptions import ConflictError, ErrorCode


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(
                "Ja existe um usuario com este RA",
                code=ErrorCode.USER_RA_ALREADY_EXISTS,
                details={"field": "ra", "value": user.ra},
            ) from exc
        await self.session.refresh(user)
        return user

    async def list_all(self) -> list[User]:
        result = await self.session.scalars(select(User).order_by(User.id))
        return list(result)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_ra(self, ra: str) -> User | None:
        statement = select(User).where(User.ra == ra)
        return await self.session.scalar(statement)

    async def update(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(
                "Ja existe um usuario com este RA",
                code=ErrorCode.USER_RA_ALREADY_EXISTS,
                details={"field": "ra", "value": user.ra},
            ) from exc
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
