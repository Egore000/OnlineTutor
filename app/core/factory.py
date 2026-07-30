from fastapi import FastAPI

from app.api.router import configure_routes
from app.core.exceptions import configure_exception_handlers
from app.core.lifespan import lifespan
from app.core.middleware import configure_middlewares
from app.shared.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        debug=settings.app.debug,
        lifespan=lifespan,
    )
    configure_middlewares(app)
    configure_exception_handlers(app)
    configure_routes(app)
    return app
