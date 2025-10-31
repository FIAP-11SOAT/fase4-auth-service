from typing import Annotated

from pydantic import BaseModel
from fastapi import Query


class AuthDto(BaseModel):
    tax_id: str = Query(..., min_length=11, max_length=14)

AuthQuery = Annotated[AuthDto, Query()]