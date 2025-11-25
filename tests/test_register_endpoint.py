import pytest
from httpx import AsyncClient

from source.models.user import User


class TestRegisterEndpoint:

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient, repository, sample_user_data):
        response = await client.post(
            "/v1/auth",
            json=sample_user_data
        )

        assert response.status_code == 201
        data = response.json()

        assert "user_id" in data
        assert data["tax_id"] == sample_user_data["tax_id"]
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]
        assert data["message"] == "User registered successfully"

        user_in_db = await repository.find_user_by_tax_id(sample_user_data["tax_id"])
        assert user_in_db is not None
        assert user_in_db["tax_id"] == sample_user_data["tax_id"]
        assert user_in_db["email"] == sample_user_data["email"]
        assert user_in_db["name"] == sample_user_data["name"]

    @pytest.mark.asyncio
    async def test_register_duplicate_user(self, client: AsyncClient, repository, sample_user_data):
        user = User.create_costumer(
            tax_id=sample_user_data["tax_id"],
            email=sample_user_data["email"],
            name=sample_user_data["name"]
        )
        await repository.create_user(user.model_dump())

        response = await client.post(
            "/v1/auth",
            json=sample_user_data
        )

        assert response.status_code == 409
        data = response.json()
        assert "detail" in data
        assert "already exists" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_missing_fields(self, client: AsyncClient):
        response = await client.post(
            "/v1/auth",
            json={"tax_id": "12345678900"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_json(self, client: AsyncClient):
        response = await client.post(
            "/v1/auth",
            content="invalid json"
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_creates_customer_user_type(self, client: AsyncClient, repository, sample_user_data):
        response = await client.post(
            "/v1/auth",
            json=sample_user_data
        )

        assert response.status_code == 201

        user_in_db = await repository.find_user_by_tax_id(sample_user_data["tax_id"])
        assert user_in_db["user_type"] == "customers"
