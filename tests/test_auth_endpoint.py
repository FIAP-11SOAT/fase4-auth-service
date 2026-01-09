import pytest
from httpx import AsyncClient

from source.models.user import User


class TestAuthEndpoint:

    @pytest.mark.asyncio
    async def test_auth_success(self, client: AsyncClient, repository, sample_user_data):
        user = User.create_costumer(
            tax_id=sample_user_data["tax_id"],
            email=sample_user_data["email"],
            name=sample_user_data["name"]
        )
        await repository.create_user(user.model_dump())

        response = await client.get(
            "/auth",
            params={"tax_id": sample_user_data["tax_id"]}
        )

        assert response.status_code == 200
        data = response.json()

        assert "token" in data
        assert data["user_id"] == user.id
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

    @pytest.mark.asyncio
    async def test_auth_user_not_found(self, client: AsyncClient):
        response = await client.get(
            "/auth",
            params={"tax_id": "99999999999"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_auth_missing_tax_id(self, client: AsyncClient):
        response = await client.get("/auth")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_auth_jwt_token_is_valid(self, client: AsyncClient, repository, jwt_signer, sample_user_data):
        user = User.create_costumer(
            tax_id=sample_user_data["tax_id"],
            email=sample_user_data["email"],
            name=sample_user_data["name"]
        )
        await repository.create_user(user.model_dump())

        response = await client.get(
            "/auth",
            params={"tax_id": sample_user_data["tax_id"]}
        )

        assert response.status_code == 200
        token = response.json()["token"]

        import json
        claims = json.loads(jwt_signer.verify(token))

        assert claims["sub"] == user.id
        assert claims["tax_id"] == user.tax_id
        assert claims["email"] == user.email
        assert claims["name"] == user.name
        assert claims["user_type"] == user.user_type.value
