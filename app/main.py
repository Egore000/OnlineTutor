import uvicorn

from app.core.factory import create_app
from app.shared.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.server.host, port=settings.server.port, reload=settings.app.debug
    )
