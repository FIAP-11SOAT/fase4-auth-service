from typing import Annotated

from fastapi.params import Depends
from fastapi.requests import Request

from source.helpers.jwt import JwtSignatureProvider


def get_jwt_provider(request: Request):
    if not hasattr(request.state, 'jwt_provider'):
        raise RuntimeError('State jwt_provider has not been set in app.lifespan')
    return request.state.jwt_provider


DependsJwtSignatureProvider = Annotated[JwtSignatureProvider, Depends(get_jwt_provider)]