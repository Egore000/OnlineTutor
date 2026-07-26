from fastapi import FastAPI
import uvicorn 

from app.shared.config import settings


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    debug=settings.server.debug,
    description="API for Tutor Management System",
)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.server.host, port=settings.server.port, reload=True)