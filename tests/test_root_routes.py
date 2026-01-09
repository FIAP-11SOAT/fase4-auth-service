import pytest
from httpx import AsyncClient
class TestRootRoutes:
    """Testes para os endpoints root"""
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Testa o endpoint raiz"""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Auth Service is running"
    @pytest.mark.asyncio
    async def test_health_endpoint(self, client: AsyncClient):
        """Testa o endpoint de health check"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Auth Service is healthy"
    @pytest.mark.asyncio
    async def test_root_returns_json(self, client: AsyncClient):
        """Verifica que o root retorna JSON"""
        response = await client.get("/")
        assert response.headers["content-type"].startswith("application/json")
    @pytest.mark.asyncio
    async def test_health_returns_json(self, client: AsyncClient):
        """Verifica que o health retorna JSON"""
        response = await client.get("/health")
        assert response.headers["content-type"].startswith("application/json")
