from fastapi import APIRouter

from source.depends.jwt_signer import DependsJwtSigner
from source.depends.repository import DependsRepository
from source.schemas.request.auth import AuthRequestQuery, AuthCreateRequestBody
from source.schemas.response.auth import AuthResponse, RegisterResponse
from source.usecase.auth import AuthUseCase, RegisterUseCase

router = APIRouter(
    prefix="/v1",
    tags=["auth"]
)


@router.get("/auth", response_model=AuthResponse)
async def auth(q: AuthRequestQuery, repo: DependsRepository, jwt_signer: DependsJwtSigner):
    use_case = AuthUseCase(repository=repo, jwt_signer=jwt_signer)
    return await use_case.execute(tax_id=q.tax_id)


@router.post("/auth", response_model=RegisterResponse, status_code=201)
async def register(body: AuthCreateRequestBody, repo: DependsRepository):
    use_case = RegisterUseCase(repository=repo)
    return await use_case.execute(tax_id=body.tax_id, email=body.email, name=body.name)
