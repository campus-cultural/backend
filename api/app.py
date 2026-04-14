from __future__ import annotations

from fastapi import FastAPI

from api.features.user.user_controller import router as user_router
from api.shared.exceptions import ResourceNotFoundError
from database.config.session import DatabaseManager


def create_app(database_url: str | None = None) -> FastAPI:
    database_manager = DatabaseManager(database_url=database_url)
    database_manager.create_tables()

    app = FastAPI(title="Campus Cultural API")
    app.state.database_manager = database_manager

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(_, exc: ResourceNotFoundError):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(user_router)
    return app


app = create_app()
