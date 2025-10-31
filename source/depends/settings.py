from typing import Annotated

from fastapi.params import Depends
from fastapi.requests import Request

from source.helpers.settings import Settings


def get_settings(request: Request):
    if not hasattr(request.state, 'settings'):
        raise RuntimeError('State settings has not been set in app.lifespan')
    return request.state.settings


DependsSettings = Annotated[Settings, Depends(get_settings)]