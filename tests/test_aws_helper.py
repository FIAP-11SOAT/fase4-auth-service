import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import orjson
from source.helpers.aws import get_aws_secrets
class TestAwsHelper:
    """Testes para o helper de AWS"""
    @pytest.mark.asyncio
    async def test_get_aws_secrets_success(self):
        """Testa get_aws_secrets com sucesso"""
        secret_name = "test-secret"
        secret_data = {
            "JWT_PRIVATE_KEY": "test-private-key",
            "DATABASE_URL": "test-db-url"
        }
        secret_string = orjson.dumps(secret_data).decode('utf-8')
        mock_client = AsyncMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': secret_string
        }
        mock_session = MagicMock()
        mock_session.client.return_value.__aenter__.return_value = mock_client
        with patch('source.helpers.aws.aioboto3.Session', return_value=mock_session):
            result = await get_aws_secrets(secret_name)
            assert result == secret_data
            assert result["JWT_PRIVATE_KEY"] == "test-private-key"
            assert result["DATABASE_URL"] == "test-db-url"
            mock_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    @pytest.mark.asyncio
    async def test_get_aws_secrets_with_different_secret_name(self):
        """Testa get_aws_secrets com nome de secret diferente"""
        secret_name = "my-custom-secret"
        secret_data = {"key": "value"}
        secret_string = orjson.dumps(secret_data).decode('utf-8')
        mock_client = AsyncMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': secret_string
        }
        mock_session = MagicMock()
        mock_session.client.return_value.__aenter__.return_value = mock_client
        with patch('source.helpers.aws.aioboto3.Session', return_value=mock_session):
            result = await get_aws_secrets(secret_name)
            assert result == secret_data
            mock_client.get_secret_value.assert_called_once_with(SecretId="my-custom-secret")
    @pytest.mark.asyncio
    async def test_get_aws_secrets_parses_json(self):
        """Testa que get_aws_secrets faz parse do JSON corretamente"""
        secret_name = "test-secret"
        secret_data = {
            "string_field": "value",
            "number_field": 123,
            "boolean_field": True,
            "array_field": [1, 2, 3],
            "object_field": {"nested": "value"}
        }
        secret_string = orjson.dumps(secret_data).decode('utf-8')
        mock_client = AsyncMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': secret_string
        }
        mock_session = MagicMock()
        mock_session.client.return_value.__aenter__.return_value = mock_client
        with patch('source.helpers.aws.aioboto3.Session', return_value=mock_session):
            result = await get_aws_secrets(secret_name)
            assert result["string_field"] == "value"
            assert result["number_field"] == 123
            assert result["boolean_field"] is True
            assert result["array_field"] == [1, 2, 3]
            assert result["object_field"]["nested"] == "value"
    @pytest.mark.asyncio
    async def test_get_aws_secrets_creates_session(self):
        """Testa que get_aws_secrets cria uma sessão aioboto3"""
        secret_name = "test-secret"
        secret_string = orjson.dumps({"key": "value"}).decode('utf-8')
        mock_client = AsyncMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': secret_string
        }
        mock_session = MagicMock()
        mock_session.client.return_value.__aenter__.return_value = mock_client
        with patch('source.helpers.aws.aioboto3.Session', return_value=mock_session) as mock_session_class:
            await get_aws_secrets(secret_name)
            mock_session_class.assert_called_once()
            mock_session.client.assert_called_once_with("secretsmanager")
