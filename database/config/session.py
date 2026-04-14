from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.features.user import user_models  # noqa: F401
from database.config.base import Base
from database.config.settings import get_database_url


class DatabaseManager:
    def __init__(self, database_url: str | None = None) -> None:
        resolved_database_url = database_url or get_database_url()
        connect_args = (
            {"check_same_thread": False} if resolved_database_url.startswith("sqlite") else {}
        )
        self.engine = create_engine(resolved_database_url, connect_args=connect_args)
        self.session_factory = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False
        )

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self.session_factory()
        try:
            yield session
        finally:
            session.close()
