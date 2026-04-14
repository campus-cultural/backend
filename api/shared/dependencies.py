from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from api.features.user.user_repository import UserRepository
from api.features.user.user_service import UserService


def get_db_session(request: Request) -> Generator[Session, None, None]:
    with request.app.state.database_manager.session() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_db_session)]


def get_user_service(session: SessionDependency) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
