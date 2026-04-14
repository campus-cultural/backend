from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.features.user.user_repository import UserRepository
from api.features.user.user_service import UserService


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async for session in request.app.state.database_manager.session():
        yield session


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)
