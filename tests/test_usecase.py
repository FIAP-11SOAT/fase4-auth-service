import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from source.usecase.auth import AuthUseCase, RegisterUseCase
from source.models.user import User, UserType
from source.schemas.response.auth import AuthResponse, RegisterResponse
class TestAuthUseCase:
    """Testes unitários para AuthUseCase"""
    @pytest.mark.asyncio
    async def test_execute_success(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_jwt_signer = MagicMock()
        user_data = {
            "id": "user-123",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User",
            "user_type": "customers"
        }
        mock_repository.find_user_by_tax_id.return_value = user_data
        mock_jwt_signer.sign.return_value = "mock_jwt_token"
        use_case = AuthUseCase(repository=mock_repository, jwt_signer=mock_jwt_signer)
        # Act
        result = await use_case.execute(tax_id="12345678900")
        # Assert
        assert isinstance(result, AuthResponse)
        assert result.token == "mock_jwt_token"
        assert result.user_id == "user-123"
        assert result.name == "Test User"
        assert result.email == "test@example.com"
        mock_repository.find_user_by_tax_id.assert_called_once_with("12345678900")
        mock_jwt_signer.sign.assert_called_once()
    @pytest.mark.asyncio
    async def test_execute_user_not_found(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_jwt_signer = MagicMock()
        mock_repository.find_user_by_tax_id.return_value = None
        use_case = AuthUseCase(repository=mock_repository, jwt_signer=mock_jwt_signer)
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(tax_id="99999999999")
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()
        mock_repository.find_user_by_tax_id.assert_called_once_with("99999999999")
        mock_jwt_signer.sign.assert_not_called()
    @pytest.mark.asyncio
    async def test_execute_jwt_payload_structure(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_jwt_signer = MagicMock()
        user_data = {
            "id": "user-123",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User",
            "user_type": "customers"
        }
        mock_repository.find_user_by_tax_id.return_value = user_data
        mock_jwt_signer.sign.return_value = "mock_jwt_token"
        use_case = AuthUseCase(repository=mock_repository, jwt_signer=mock_jwt_signer)
        # Act
        await use_case.execute(tax_id="12345678900")
        # Assert - verify the JWT payload structure
        call_args = mock_jwt_signer.sign.call_args[0][0]
        assert call_args["sub"] == "user-123"
        assert call_args["tax_id"] == "12345678900"
        assert call_args["email"] == "test@example.com"
        assert call_args["name"] == "Test User"
        assert call_args["user_type"] == "customers"
    @pytest.mark.asyncio
    async def test_execute_with_employee_user_type(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_jwt_signer = MagicMock()
        user_data = {
            "id": "user-456",
            "tax_id": "98765432100",
            "email": "employee@example.com",
            "name": "Employee User",
            "user_type": "employees"
        }
        mock_repository.find_user_by_tax_id.return_value = user_data
        mock_jwt_signer.sign.return_value = "employee_jwt_token"
        use_case = AuthUseCase(repository=mock_repository, jwt_signer=mock_jwt_signer)
        # Act
        result = await use_case.execute(tax_id="98765432100")
        # Assert
        assert result.user_id == "user-456"
        call_args = mock_jwt_signer.sign.call_args[0][0]
        assert call_args["user_type"] == "employees"
class TestRegisterUseCase:
    """Testes unitários para RegisterUseCase"""
    @pytest.mark.asyncio
    async def test_execute_success(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.find_user_by_tax_id.return_value = None
        mock_repository.create_user.return_value = None
        use_case = RegisterUseCase(repository=mock_repository)
        # Act
        result = await use_case.execute(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        # Assert
        assert isinstance(result, RegisterResponse)
        assert result.tax_id == "12345678900"
        assert result.email == "test@example.com"
        assert result.name == "Test User"
        assert result.message == "User registered successfully"
        assert result.user_id is not None
        mock_repository.find_user_by_tax_id.assert_called_once_with("12345678900")
        mock_repository.create_user.assert_called_once()
    @pytest.mark.asyncio
    async def test_execute_creates_customer_user(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.find_user_by_tax_id.return_value = None
        mock_repository.create_user.return_value = None
        use_case = RegisterUseCase(repository=mock_repository)
        # Act
        await use_case.execute(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        # Assert - verify that a customer user type was created
        call_args = mock_repository.create_user.call_args[0][0]
        assert call_args["user_type"] == "customers"
    @pytest.mark.asyncio
    async def test_execute_user_already_exists(self):
        # Arrange
        mock_repository = AsyncMock()
        existing_user = {
            "id": "existing-user-id",
            "tax_id": "12345678900",
            "email": "existing@example.com",
            "name": "Existing User",
            "user_type": "customers"
        }
        mock_repository.find_user_by_tax_id.return_value = existing_user
        use_case = RegisterUseCase(repository=mock_repository)
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await use_case.execute(
                tax_id="12345678900",
                email="test@example.com",
                name="Test User"
            )
        assert exc_info.value.status_code == 409
        assert "already exists" in exc_info.value.detail.lower()
        mock_repository.find_user_by_tax_id.assert_called_once_with("12345678900")
        mock_repository.create_user.assert_not_called()
    @pytest.mark.asyncio
    async def test_execute_generates_unique_user_id(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.find_user_by_tax_id.return_value = None
        mock_repository.create_user.return_value = None
        use_case = RegisterUseCase(repository=mock_repository)
        # Act
        result1 = await use_case.execute(
            tax_id="11111111111",
            email="user1@example.com",
            name="User One"
        )
        result2 = await use_case.execute(
            tax_id="22222222222",
            email="user2@example.com",
            name="User Two"
        )
        # Assert
        assert result1.user_id != result2.user_id
    @pytest.mark.asyncio
    async def test_execute_user_data_stored_correctly(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.find_user_by_tax_id.return_value = None
        mock_repository.create_user.return_value = None
        use_case = RegisterUseCase(repository=mock_repository)
        # Act
        result = await use_case.execute(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        # Assert - verify the data stored in repository
        call_args = mock_repository.create_user.call_args[0][0]
        assert call_args["id"] == result.user_id
        assert call_args["tax_id"] == "12345678900"
        assert call_args["email"] == "test@example.com"
        assert call_args["name"] == "Test User"
        assert call_args["user_type"] == "customers"
    @pytest.mark.asyncio
    async def test_execute_with_special_characters(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.find_user_by_tax_id.return_value = None
        mock_repository.create_user.return_value = None
        use_case = RegisterUseCase(repository=mock_repository)
        # Act
        result = await use_case.execute(
            tax_id="123.456.789-00",
            email="test+tag@example.com",
            name="João da Silva"
        )
        # Assert
        assert result.tax_id == "123.456.789-00"
        assert result.email == "test+tag@example.com"
        assert result.name == "João da Silva"
