import pytest
from unittest.mock import MagicMock
from fastapi import Request
from source.depends.app import get_settings, get_secrets, get_services
from source.depends.jwt_signer import get_jwt_signer
from source.depends.repository import get_repository
from source.configs.settings import Settings
from source.configs.secrets import Secrets
from source.configs.services import Services
from source.helpers.jwt import JwtSignatureProvider
from source.helpers.repository import AsyncDatabaseRepository
class TestAppDependencies:
    """Testes para as dependências da aplicação"""
    def test_get_settings_success(self):
        """Testa get_settings quando settings está no state"""
        request = MagicMock(spec=Request)
        settings = Settings()
        request.state.settings = settings
        result = get_settings(request)
        assert result is settings
    def test_get_settings_not_set(self):
        """Testa get_settings quando settings não está no state"""
        request = MagicMock(spec=Request)
        delattr(request.state, 'settings')
        with pytest.raises(RuntimeError) as exc_info:
            get_settings(request)
        assert "settings has not been set" in str(exc_info.value)
    def test_get_secrets_success(self):
        """Testa get_secrets quando secrets está no state"""
        request = MagicMock(spec=Request)
        secrets = Secrets(jwt_private_key="test-key")
        request.state.secrets = secrets
        result = get_secrets(request)
        assert result is secrets
    def test_get_secrets_not_set(self):
        """Testa get_secrets quando secrets não está no state"""
        request = MagicMock(spec=Request)
        delattr(request.state, 'secrets')
        with pytest.raises(RuntimeError) as exc_info:
            get_secrets(request)
        assert "secrets has not been set" in str(exc_info.value)
    def test_get_services_success(self):
        """Testa get_services quando services está no state"""
        request = MagicMock(spec=Request)
        services = Services()
        request.state.services = services
        result = get_services(request)
        assert result is services
    def test_get_services_not_set(self):
        """Testa get_services quando services não está no state"""
        request = MagicMock(spec=Request)
        delattr(request.state, 'services')
        with pytest.raises(RuntimeError) as exc_info:
            get_services(request)
        assert "services has not been set" in str(exc_info.value)
class TestJwtSignerDependency:
    """Testes para a dependência do JWT Signer"""
    def test_get_jwt_signer_success(self, jwt_signer):
        """Testa get_jwt_signer quando jwt_signer está inicializado"""
        services = Services()
        services.jwt_signer = jwt_signer
        result = get_jwt_signer(services)
        assert result is jwt_signer
    def test_get_jwt_signer_not_initialized(self):
        """Testa get_jwt_signer quando jwt_signer não está inicializado"""
        services = Services()
        services.jwt_signer = None
        with pytest.raises(RuntimeError) as exc_info:
            get_jwt_signer(services)
        assert "JWT Signer has not been initialized" in str(exc_info.value)
class TestRepositoryDependency:
    """Testes para a dependência do Repository"""
    @pytest.mark.asyncio
    async def test_get_repository_success(self, repository):
        """Testa get_repository quando repository está inicializado"""
        services = Services()
        services.repository = repository
        result = get_repository(services)
        assert result is repository
    def test_get_repository_not_initialized(self):
        """Testa get_repository quando repository não está inicializado"""
        services = Services()
        services.repository = None
        with pytest.raises(RuntimeError) as exc_info:
            get_repository(services)
        assert "Repository has not been initialized" in str(exc_info.value)
