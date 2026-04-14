from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from database.config.base import Base
from database.config.settings import get_database_url


class DatabaseManager:
    def __init__(self, database_url: str | None = None) -> None:
        resolved_database_url = self._to_async_database_url(database_url or get_database_url())
        connect_args = (
            {"check_same_thread": False} if resolved_database_url.startswith("sqlite") else {}
        )
        self.engine: AsyncEngine = create_async_engine(
            resolved_database_url,
            connect_args=connect_args,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @staticmethod
    def _to_async_database_url(database_url: str) -> str:
        if database_url.startswith("sqlite:///") and not database_url.startswith(
            "sqlite+aiosqlite:///"
        ):
            return database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        return database_url

    async def create_tables(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
