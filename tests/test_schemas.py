import pytest
from pydantic import ValidationError

from source.schemas.request.auth import AuthRequest, AuthCreateRequest
from source.schemas.response.auth import AuthResponse, RegisterResponse


class TestAuthRequestSchema:
    """Testes para o schema AuthRequest"""

    def test_auth_request_valid(self):
        data = {"tax_id": "12345678900"}
        request = AuthRequest(**data)
        assert request.tax_id == "12345678900"

    def test_auth_request_missing_tax_id(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthRequest()
        assert "tax_id" in str(exc_info.value)

    def test_auth_request_empty_tax_id(self):
        # Pydantic accepts empty string unless we add validators
        request = AuthRequest(tax_id="")
        assert request.tax_id == ""

    def test_auth_request_model_dump(self):
        request = AuthRequest(tax_id="12345678900")
        dumped = request.model_dump()
        assert dumped == {"tax_id": "12345678900"}


class TestAuthCreateRequestSchema:
    """Testes para o schema AuthCreateRequest"""

    def test_auth_create_request_valid(self):
        data = {
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User"
        }
        request = AuthCreateRequest(**data)
        assert request.tax_id == "12345678900"
        assert request.email == "test@example.com"
        assert request.name == "Test User"

    def test_auth_create_request_missing_tax_id(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthCreateRequest(email="test@example.com", name="Test User")
        assert "tax_id" in str(exc_info.value)

    def test_auth_create_request_missing_email(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthCreateRequest(tax_id="12345678900", name="Test User")
        assert "email" in str(exc_info.value)

    def test_auth_create_request_missing_name(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthCreateRequest(tax_id="12345678900", email="test@example.com")
        assert "name" in str(exc_info.value)

    def test_auth_create_request_all_missing(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthCreateRequest()
        errors = str(exc_info.value)
        assert "tax_id" in errors
        assert "email" in errors
        assert "name" in errors

    def test_auth_create_request_model_dump(self):
        request = AuthCreateRequest(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        dumped = request.model_dump()
        assert dumped == {
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User"
        }


class TestAuthResponseSchema:
    """Testes para o schema AuthResponse"""

    def test_auth_response_valid(self):
        data = {
            "token": "eyJhbGciOiJSUzI1NiJ9...",
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test User",
            "email": "test@example.com"
        }
        response = AuthResponse(**data)
        assert response.token == "eyJhbGciOiJSUzI1NiJ9..."
        assert response.user_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.name == "Test User"
        assert response.email == "test@example.com"

    def test_auth_response_missing_token(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthResponse(
                user_id="123",
                name="Test User",
                email="test@example.com"
            )
        assert "token" in str(exc_info.value)

    def test_auth_response_missing_user_id(self):
        with pytest.raises(ValidationError) as exc_info:
            AuthResponse(
                token="token123",
                name="Test User",
                email="test@example.com"
            )
        assert "user_id" in str(exc_info.value)

    def test_auth_response_model_dump(self):
        response = AuthResponse(
            token="token123",
            user_id="user123",
            name="Test User",
            email="test@example.com"
        )
        dumped = response.model_dump()
        assert dumped == {
            "token": "token123",
            "user_id": "user123",
            "name": "Test User",
            "email": "test@example.com"
        }


class TestRegisterResponseSchema:
    """Testes para o schema RegisterResponse"""

    def test_register_response_valid(self):
        data = {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User"
        }
        response = RegisterResponse(**data)
        assert response.user_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.tax_id == "12345678900"
        assert response.email == "test@example.com"
        assert response.name == "Test User"
        assert response.message == "User registered successfully"

    def test_register_response_custom_message(self):
        data = {
            "user_id": "123",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User",
            "message": "Custom success message"
        }
        response = RegisterResponse(**data)
        assert response.message == "Custom success message"

    def test_register_response_missing_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            RegisterResponse(user_id="123")
        errors = str(exc_info.value)
        assert "tax_id" in errors
        assert "email" in errors
        assert "name" in errors

    def test_register_response_model_dump(self):
        response = RegisterResponse(
            user_id="user123",
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        dumped = response.model_dump()
        assert dumped == {
            "user_id": "user123",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User",
            "message": "User registered successfully"
        }

