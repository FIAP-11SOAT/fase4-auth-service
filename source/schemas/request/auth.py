from typing import Annotated, TypeAlias

from fastapi import Query, Body
from pydantic import BaseModel


class AuthRequest(BaseModel):
    tax_id: str = Query(..., description="CPF do usuário")


AuthRequestQuery: TypeAlias = Annotated[AuthRequest, Query(...)]


class AuthCreateRequest(BaseModel):
    tax_id: str = Body(..., description="CPF do usuário")
    email: str = Body(..., description="Email do usuário")
    name: str = Body(..., description="Nome completo do usuário")


AuthCreateRequestBody: TypeAlias = Annotated[AuthCreateRequest, Body(...)]
