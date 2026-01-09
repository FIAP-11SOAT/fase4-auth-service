from fastapi import HTTPException, status

from source.helpers.jwt import JwtSignatureProvider
from source.helpers.repository import AsyncDatabaseRepository
from source.models.user import User
from source.schemas.response.auth import AuthResponse, RegisterResponse


class AuthUseCase:

    def __init__(self, repository: AsyncDatabaseRepository, jwt_signer: JwtSignatureProvider):
        self.repository = repository
        self.jwt_signer = jwt_signer

    async def execute(self, tax_id: str) -> AuthResponse:
        user_data = await self.repository.find_user_by_tax_id(tax_id)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with tax_id {tax_id} not found"
            )

        payload = {
            "sub": user_data["id"],
            "tax_id": user_data["tax_id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "user_type": user_data["user_type"]
        }

        token = self.jwt_signer.sign(payload)

        return AuthResponse(
            token=token,
            user_id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"]
        )


class RegisterUseCase:

    def __init__(self, repository: AsyncDatabaseRepository):
        self.repository = repository

    async def execute(self, tax_id: str, email: str, name: str) -> RegisterResponse:
        existing_user = await self.repository.find_user_by_tax_id(tax_id)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with tax_id {tax_id} already exists"
            )

        user = User.create_costumer(tax_id=tax_id, email=email, name=name)

        await self.repository.create_user(user.model_dump())

        return RegisterResponse(
            user_id=user.id,
            tax_id=user.tax_id,
            email=user.email,
            name=user.name
        )
