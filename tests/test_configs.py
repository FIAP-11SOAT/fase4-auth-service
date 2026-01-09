import pytest
from unittest.mock import patch, AsyncMock
from source.configs.settings import Settings
from source.configs.secrets import Secrets
class TestSettings:
    """Testes para a classe Settings"""
    def test_settings_default_values(self):
        """Testa os valores padrão das configurações"""
        settings = Settings()
        assert settings.profile == "development"
        assert settings.short_profile == "dev"
        assert settings.application_name == "fase4-auth-service"
        assert settings.application_secret_name == "fase4-auth-service-secrets"
        assert settings.application_table_name == "fase4-auth-service-users"
        assert settings.version is not None
    def test_settings_new_development(self):
        """Testa criação de settings para development"""
        with patch.dict('os.environ', {'PROFILE': 'development'}):
            settings = Settings.new()
            assert settings.profile == "development"
            assert settings.short_profile == "dev"
    def test_settings_new_staging(self):
        """Testa criação de settings para staging"""
        with patch.dict('os.environ', {'PROFILE': 'staging'}):
            settings = Settings(profile="staging")
            settings = Settings.new()
            assert settings.short_profile == "stg"
    def test_settings_new_production(self):
        """Testa criação de settings para production"""
        with patch.dict('os.environ', {'PROFILE': 'production'}):
            settings = Settings(profile="production")
            settings = Settings.new()
            assert settings.short_profile == "prod"
    def test_settings_invalid_profile(self):
        """Testa profile inválido"""
        with patch.dict('os.environ', {'PROFILE': 'invalid'}):
            settings = Settings(profile="invalid")
            with pytest.raises(ValueError) as exc_info:
                Settings.new()
            assert "Invalid profile" in str(exc_info.value)
    def test_settings_profile_mapping(self):
        """Testa o mapeamento de profiles"""
        assert "development" in Settings.__map_profile_to_short__
        assert "staging" in Settings.__map_profile_to_short__
        assert "production" in Settings.__map_profile_to_short__
        assert Settings.__map_profile_to_short__["development"] == "dev"
        assert Settings.__map_profile_to_short__["staging"] == "stg"
        assert Settings.__map_profile_to_short__["production"] == "prod"
class TestSecrets:
    """Testes para a classe Secrets"""
    def test_secrets_dataclass(self):
        """Testa se Secrets é um dataclass válido"""
        secrets = Secrets(jwt_private_key="test-key")
        assert secrets.jwt_private_key == "test-key"
    @pytest.mark.asyncio
    async def test_secrets_new_success(self):
        """Testa criação de secrets com sucesso"""
        settings = Settings()
        mock_secrets = {
            "JWT_PRIVATE_KEY": "mock-private-key-value"
        }
        with patch('source.configs.secrets.get_aws_secrets', new_callable=AsyncMock) as mock_get_secrets:
            mock_get_secrets.return_value = mock_secrets
            secrets = await Secrets.new(settings)
            assert secrets.jwt_private_key == "mock-private-key-value"
            mock_get_secrets.assert_called_once_with(settings.application_secret_name)
    @pytest.mark.asyncio
    async def test_secrets_new_calls_aws(self):
        """Testa que Secrets.new chama o AWS Secrets Manager"""
        settings = Settings(application_secret_name="test-secret-name")
        mock_secrets = {"JWT_PRIVATE_KEY": "test-key"}
        with patch('source.configs.secrets.get_aws_secrets', new_callable=AsyncMock) as mock_get_secrets:
            mock_get_secrets.return_value = mock_secrets
            await Secrets.new(settings)
            mock_get_secrets.assert_called_once_with("test-secret-name")
