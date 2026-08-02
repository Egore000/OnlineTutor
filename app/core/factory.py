from fastapi import FastAPI

from app.api.router import configure_routes
from app.core.exceptions import configure_exception_handlers
from app.core.lifespan import lifespan
from app.core.middleware import configure_middlewares
from app.shared.config import AppSettings

settings = AppSettings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.name,
        summary=settings.summary,
        description=settings.description,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    configure_middlewares(app)
    configure_exception_handlers(app)
    configure_routes(app)
    return app
