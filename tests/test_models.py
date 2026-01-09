import pytest
import uuid
from pydantic import ValidationError
from source.models.user import User, UserType
class TestUserType:
    """Testes para o enum UserType"""
    def test_user_type_customers(self):
        assert UserType.CUSTOMERS == "customers"
        assert UserType.CUSTOMERS.value == "customers"
    def test_user_type_employees(self):
        assert UserType.EMPLOYEES == "employees"
        assert UserType.EMPLOYEES.value == "employees"
    def test_user_type_from_string(self):
        assert UserType("customers") == UserType.CUSTOMERS
        assert UserType("employees") == UserType.EMPLOYEES
    def test_user_type_invalid_value(self):
        with pytest.raises(ValueError):
            UserType("invalid_type")
    def test_user_type_enum_members(self):
        members = list(UserType)
        assert len(members) == 2
        assert UserType.CUSTOMERS in members
        assert UserType.EMPLOYEES in members
class TestUserModel:
    """Testes para o modelo User"""
    def test_user_creation_valid(self):
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            tax_id="12345678900",
            email="test@example.com",
            name="Test User",
            user_type=UserType.CUSTOMERS
        )
        assert user.id == user_id
        assert user.tax_id == "12345678900"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.user_type == UserType.CUSTOMERS
    def test_user_creation_missing_id(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                tax_id="12345678900",
                email="test@example.com",
                name="Test User",
                user_type=UserType.CUSTOMERS
            )
        assert "id" in str(exc_info.value)
    def test_user_creation_missing_tax_id(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                id=str(uuid.uuid4()),
                email="test@example.com",
                name="Test User",
                user_type=UserType.CUSTOMERS
            )
        assert "tax_id" in str(exc_info.value)
    def test_user_creation_missing_email(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                id=str(uuid.uuid4()),
                tax_id="12345678900",
                name="Test User",
                user_type=UserType.CUSTOMERS
            )
        assert "email" in str(exc_info.value)
    def test_user_creation_missing_name(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                id=str(uuid.uuid4()),
                tax_id="12345678900",
                email="test@example.com",
                user_type=UserType.CUSTOMERS
            )
        assert "name" in str(exc_info.value)
    def test_user_creation_missing_user_type(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                id=str(uuid.uuid4()),
                tax_id="12345678900",
                email="test@example.com",
                name="Test User"
            )
        assert "user_type" in str(exc_info.value)
    def test_user_creation_invalid_user_type(self):
        with pytest.raises(ValidationError) as exc_info:
            User(
                id=str(uuid.uuid4()),
                tax_id="12345678900",
                email="test@example.com",
                name="Test User",
                user_type="invalid_type"
            )
        assert "user_type" in str(exc_info.value)
    def test_user_with_employees_type(self):
        user = User(
            id=str(uuid.uuid4()),
            tax_id="12345678900",
            email="employee@example.com",
            name="Employee User",
            user_type=UserType.EMPLOYEES
        )
        assert user.user_type == UserType.EMPLOYEES
class TestUserCreateCostumer:
    """Testes para o método create_costumer"""
    def test_create_customer_valid(self):
        user = User.create_costumer(
            tax_id="12345678900",
            email="customer@example.com",
            name="Customer User"
        )
        assert user.tax_id == "12345678900"
        assert user.email == "customer@example.com"
        assert user.name == "Customer User"
        assert user.user_type == UserType.CUSTOMERS
        assert user.id is not None
        assert isinstance(user.id, str)
    def test_create_customer_generates_unique_ids(self):
        user1 = User.create_costumer(
            tax_id="11111111111",
            email="user1@example.com",
            name="User One"
        )
        user2 = User.create_costumer(
            tax_id="22222222222",
            email="user2@example.com",
            name="User Two"
        )
        assert user1.id != user2.id
    def test_create_customer_generates_valid_uuid(self):
        user = User.create_costumer(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        # Validate that the ID is a valid UUID
        try:
            uuid.UUID(user.id)
        except ValueError:
            pytest.fail("User ID is not a valid UUID")
    def test_create_customer_model_dump(self):
        user = User.create_costumer(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        dumped = user.model_dump()
        assert dumped["tax_id"] == "12345678900"
        assert dumped["email"] == "test@example.com"
        assert dumped["name"] == "Test User"
        assert dumped["user_type"] == "customers"
        assert "id" in dumped
    def test_create_customer_is_pydantic_model(self):
        user = User.create_costumer(
            tax_id="12345678900",
            email="test@example.com",
            name="Test User"
        )
        # Test that it's a proper Pydantic model
        assert hasattr(user, "model_dump")
        assert hasattr(user, "model_validate")
    def test_create_customer_with_empty_strings(self):
        # Pydantic will accept empty strings unless we add validators
        user = User.create_costumer(
            tax_id="",
            email="",
            name=""
        )
        assert user.tax_id == ""
        assert user.email == ""
        assert user.name == ""
    def test_create_customer_with_special_characters(self):
        user = User.create_costumer(
            tax_id="123.456.789-00",
            email="test+tag@example.com",
            name="João da Silva"
        )
        assert user.tax_id == "123.456.789-00"
        assert user.email == "test+tag@example.com"
        assert user.name == "João da Silva"
