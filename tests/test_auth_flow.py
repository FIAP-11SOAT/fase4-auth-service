import pytest
from httpx import AsyncClient


class TestAuthFlow:

    @pytest.mark.asyncio
    async def test_register_then_auth(self, client: AsyncClient, sample_user_data):
        register_response = await client.post(
            "/auth",
            json=sample_user_data
        )

        assert register_response.status_code == 201
        register_data = register_response.json()
        user_id = register_data["user_id"]

        auth_response = await client.get(
            "/auth",
            params={"tax_id": sample_user_data["tax_id"]}
        )

        assert auth_response.status_code == 200
        auth_data = auth_response.json()

        assert auth_data["user_id"] == user_id
        assert auth_data["name"] == sample_user_data["name"]
        assert auth_data["email"] == sample_user_data["email"]
        assert "token" in auth_data

    @pytest.mark.asyncio
    async def test_multiple_users_registration(self, client: AsyncClient, repository):
        users = [
            {"tax_id": "11111111111", "email": "user1@example.com", "name": "User One"},
            {"tax_id": "22222222222", "email": "user2@example.com", "name": "User Two"},
            {"tax_id": "33333333333", "email": "user3@example.com", "name": "User Three"},
        ]

        for user_data in users:
            response = await client.post("/auth", json=user_data)
            assert response.status_code == 201

        for user_data in users:
            auth_response = await client.get(
                "/auth",
                params={"tax_id": user_data["tax_id"]}
            )
            assert auth_response.status_code == 200
            assert auth_response.json()["email"] == user_data["email"]
