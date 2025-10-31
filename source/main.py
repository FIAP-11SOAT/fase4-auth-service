from contextlib import asynccontextmanager

from fastapi import FastAPI

from source.helpers.aws import get_aws_secrets
from source.helpers.jwt import JwtSignatureProvider
from source.helpers.settings import Settings

from source.routes import auth, root


@asynccontextmanager
async def app_lifespan(_app: FastAPI):
    secrets = get_aws_secrets("fase4-auth-service-secrets")
    settings = Settings.from_dict(secrets=secrets)
    jwt_provider = JwtSignatureProvider(private_key=settings.private_key)
    yield {"settings": settings, "jwt_provider": jwt_provider}

app = FastAPI(lifespan=app_lifespan)
app.include_router(root.router)
app.include_router(auth.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("source.main:app", host="0.0.0.0", port=8000, reload=True)

