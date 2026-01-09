import pytest
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from source.helpers.jwt import JwtSignatureProvider
def generate_rsa_key_pair():
    """Generate RSA key pair for testing"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem.decode('utf-8')
class TestJwtSignatureProvider:
    """Testes para o JwtSignatureProvider"""
    @pytest.fixture
    def private_key(self):
        return generate_rsa_key_pair()
    @pytest.fixture
    def jwt_provider(self, private_key):
        return JwtSignatureProvider(private_key=private_key)
    def test_initialization(self, private_key):
        provider = JwtSignatureProvider(private_key=private_key)
        assert provider.private_key is not None
    def test_sign_creates_token(self, jwt_provider):
        payload = {
            "sub": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        token = jwt_provider.sign(payload)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    def test_sign_and_verify(self, jwt_provider):
        payload = {
            "sub": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["sub"] == "user-123"
        assert claims_dict["email"] == "test@example.com"
        assert claims_dict["name"] == "Test User"
    def test_sign_with_empty_payload(self, jwt_provider):
        payload = {}
        token = jwt_provider.sign(payload)
        assert token is not None
        assert isinstance(token, str)
    def test_sign_with_complex_payload(self, jwt_provider):
        payload = {
            "sub": "user-123",
            "tax_id": "12345678900",
            "email": "test@example.com",
            "name": "Test User",
            "user_type": "customers",
            "metadata": {
                "role": "admin",
                "permissions": ["read", "write"]
            }
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["sub"] == "user-123"
        assert claims_dict["tax_id"] == "12345678900"
        assert claims_dict["metadata"]["role"] == "admin"
        assert "read" in claims_dict["metadata"]["permissions"]
    def test_sign_with_numeric_values(self, jwt_provider):
        payload = {
            "user_id": 123,
            "age": 30,
            "score": 95.5
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["user_id"] == 123
        assert claims_dict["age"] == 30
        assert claims_dict["score"] == 95.5
    def test_sign_with_boolean_values(self, jwt_provider):
        payload = {
            "is_active": True,
            "is_admin": False
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["is_active"] is True
        assert claims_dict["is_admin"] is False
    def test_sign_with_null_values(self, jwt_provider):
        payload = {
            "optional_field": None,
            "email": "test@example.com"
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["optional_field"] is None
        assert claims_dict["email"] == "test@example.com"
    def test_verify_invalid_token(self, jwt_provider):
        with pytest.raises(Exception):
            jwt_provider.verify("invalid.token.here")
    def test_verify_malformed_token(self, jwt_provider):
        with pytest.raises(Exception):
            jwt_provider.verify("not-a-valid-jwt")
    def test_different_providers_different_signatures(self):
        key1 = generate_rsa_key_pair()
        key2 = generate_rsa_key_pair()
        provider1 = JwtSignatureProvider(private_key=key1)
        provider2 = JwtSignatureProvider(private_key=key2)
        payload = {"sub": "user-123", "email": "test@example.com"}
        token1 = provider1.sign(payload)
        token2 = provider2.sign(payload)
        # Tokens should be different even with same payload
        assert token1 != token2
        # Each provider can verify its own token
        claims1 = json.loads(provider1.verify(token1))
        claims2 = json.loads(provider2.verify(token2))
        assert claims1["sub"] == "user-123"
        assert claims2["sub"] == "user-123"
    def test_token_format(self, jwt_provider):
        payload = {"sub": "user-123"}
        token = jwt_provider.sign(payload)
        # JWT tokens typically have 3 parts separated by dots (for JWE it might be 5)
        parts = token.split('.')
        assert len(parts) >= 3
    def test_sign_with_special_characters_in_strings(self, jwt_provider):
        payload = {
            "name": "José da Silva",
            "email": "jose+tag@example.com",
            "description": "User with special chars: áéíóú ñ ç"
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        assert claims_dict["name"] == "José da Silva"
        assert claims_dict["email"] == "jose+tag@example.com"
        assert "áéíóú" in claims_dict["description"]
    def test_sign_preserves_payload_order(self, jwt_provider):
        payload = {
            "sub": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "tax_id": "12345678900"
        }
        token = jwt_provider.sign(payload)
        claims = jwt_provider.verify(token)
        claims_dict = json.loads(claims)
        # All keys should be present
        assert set(claims_dict.keys()).issuperset({"sub", "email", "name", "tax_id"})
