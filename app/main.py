import uvicorn

from app.core.factory import create_app
from app.shared.config import AppSettings, ServerSettings

server_settings = ServerSettings()
app_settings = AppSettings()

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=server_settings.host,
        port=server_settings.port,
        reload=app_settings.debug,
        access_log=False,
    )
