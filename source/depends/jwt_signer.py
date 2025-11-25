from typing import Annotated, TypeAlias

from fastapi import Depends

from source.depends.app import DependsServices
from source.helpers.jwt import JwtSignatureProvider


def get_jwt_signer(services: DependsServices):
    if not services.jwt_signer:
        raise RuntimeError('JWT Signer has not been initialized in app.lifespan')
    return services.jwt_signer


DependsJwtSigner: TypeAlias = Annotated[JwtSignatureProvider, Depends(get_jwt_signer)]
