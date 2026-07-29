import logging
import time
from collections.abc import Callable

from fastapi import FastAPI, Request, Response

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next: Callable[..., Response]) -> Response:
    """Middleware для логирования запроса"""

    start_time = time.perf_counter()

    response = call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        "HTTP запрос выполнен",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": process_time,
            "client_id": request.client,
        },
    )
    return response


def configure_middlewares(app: FastAPI) -> None:
    """Конфигурация Middlewares"""

    app.middleware("http")(log_requests)
