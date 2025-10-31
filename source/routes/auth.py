import boto3
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from source.depends.jwt_provider import DependsJwtSignatureProvider
from source.dtos.auth import AuthQuery
from source.helpers.repository import DatabaseRepository

router = APIRouter()

@router.get("/auth")
def login(jwt_provider: DependsJwtSignatureProvider, query: AuthQuery):
    repository = DatabaseRepository(
        resource=boto3.resource("dynamodb"),
        table_name="fase4-auth-service-users",
    )
    result = repository.find_user_by_tax_id(tax_id=query.tax_id)
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"query": query.model_dump(), "user": result},
    )


@router.post("/auth")
def register():
    pass