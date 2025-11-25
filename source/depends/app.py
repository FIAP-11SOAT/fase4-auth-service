from typing import Annotated, TypeAlias

from fastapi.params import Depends
from fastapi.requests import Request

from source.configs.secrets import Secrets
from source.configs.services import Services
from source.configs.settings import Settings


def get_settings(request: Request):
    if not hasattr(request.state, 'settings'):
        raise RuntimeError('State settings has not been set in app.lifespan')
    return request.state.settings


DependsSettings: TypeAlias = Annotated[Settings, Depends(get_settings)]


def get_secrets(request: Request):
    if not hasattr(request.state, 'secrets'):
        raise RuntimeError('State secrets has not been set in app.lifespan')
    return request.state.secrets


DependsSecrets: TypeAlias = Annotated[Secrets, Depends(get_secrets)]


def get_services(request: Request):
    if not hasattr(request.state, 'services'):
        raise RuntimeError('State services has not been set in app.lifespan')
    return request.state.services


DependsServices: TypeAlias = Annotated[Services, Depends(get_services)]
