from contextlib import asynccontextmanager

from fastapi import FastAPI

from source.configs.secrets import Secrets
from source.configs.services import Services
from source.configs.settings import Settings
from source.routes import auth, root


@asynccontextmanager
async def app_lifespan(_app: FastAPI):
    settings = Settings.new()
    secrets = await Secrets.new(settings=settings)
    services = Services.new(settings=settings, secrets=secrets)

    yield {
        "settings": settings,
        "secrets": secrets,
        "services": services,
    }


app = FastAPI(lifespan=app_lifespan, docs_url="/auth/docs", redoc_url="/auth/redoc", openapi_url="/auth/openapi.json")
app.include_router(root.router)
app.include_router(auth.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, access_log=False)
