from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.features.user.user_controller import router as user_router
from api.features.user.user_repository import UserRepository
from api.features.user.user_service import UserService
from api.shared.exceptions import register_exception_handlers
from database.config.session import DatabaseManager


def create_app(database_url: str | None = None) -> FastAPI:
    database_manager = DatabaseManager(database_url=database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.database_manager = database_manager
        await database_manager.create_tables()
        async with database_manager.session_factory() as session:
            service = UserService(UserRepository(session))
            await service.ensure_default_admin()
        yield

    app = FastAPI(title="Campus Cultural API", lifespan=lifespan)
    register_exception_handlers(app)

    @app.get("/health")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(user_router)
    return app


app = create_app()
