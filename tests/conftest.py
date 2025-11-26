import os
import pytest
import pytest_asyncio
from testcontainers.localstack import LocalStackContainer
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from contextlib import asynccontextmanager

from source.helpers.repository import AsyncDatabaseRepository
from source.helpers.jwt import JwtSignatureProvider
from source.configs.services import Services


def generate_test_rsa_key_pair():
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


@pytest.fixture(scope="session")
def dynamodb_endpoint():
    """Provide DynamoDB endpoint URL"""
    if os.getenv("CI"):
        yield "http://dynamodb:8000"
    else:
        with LocalStackContainer(image="localstack/localstack:latest") as localstack:
            localstack.with_services("dynamodb")
            yield localstack.get_url()


@pytest.fixture(scope="session")
def aws_credentials(dynamodb_endpoint):
    """Set AWS credentials for testing"""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ENDPOINT_URL"] = dynamodb_endpoint

    return {
        "endpoint_url": dynamodb_endpoint,
        "region_name": "us-east-1"
    }


@pytest.fixture(scope="session")
def test_private_key():
    """Generate test RSA private key"""
    return generate_test_rsa_key_pair()


@pytest_asyncio.fixture(scope="function")
async def repository(aws_credentials):
    """Create repository instance with test database"""

    class TestAsyncDatabaseRepository(AsyncDatabaseRepository):
        """Repository that uses localstack endpoint"""

        @asynccontextmanager
        async def get_table(self):
            async with self.session.resource(
                'dynamodb',
                region_name=self.region_name,
                endpoint_url=aws_credentials["endpoint_url"]
            ) as dynamodb:
                table = await dynamodb.Table(self.table_name)
                yield table

        async def create_table_if_not_exists(self):
            async with self.session.resource(
                'dynamodb',
                region_name=self.region_name,
                endpoint_url=aws_credentials["endpoint_url"]
            ) as dynamodb:
                existing_tables = []
                async for table in dynamodb.tables.all():
                    existing_tables.append(table.name)

                if self.table_name in existing_tables:
                    return False

                table = await dynamodb.create_table(
                    TableName=self.table_name,
                    BillingMode='PAY_PER_REQUEST',
                    KeySchema=[
                        {'AttributeName': 'id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'id', 'AttributeType': 'S'},
                        {'AttributeName': 'tax_id', 'AttributeType': 'S'}
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'TaxIDIndex',
                            'KeySchema': [
                                {'AttributeName': 'tax_id', 'KeyType': 'HASH'}
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL'
                            }
                        }
                    ],
                )

                # Wait for table to be active
                await table.wait_until_exists()
                return True

        async def clear_table(self):
            """Delete all items from the table"""
            async with self.get_table() as table:
                # Scan to get all items
                response = await table.scan()
                items = response.get('Items', [])

                # Delete each item
                for item in items:
                    await table.delete_item(Key={'id': item['id']})

    repo = TestAsyncDatabaseRepository(
        table_name="test-auth-service-users",
        region_name=aws_credentials["region_name"]
    )

    # Create table
    await repo.create_table_if_not_exists()

    # Clear any existing data
    await repo.clear_table()

    yield repo

    # Clean up after test
    await repo.clear_table()


@pytest.fixture(scope="function")
def jwt_signer(test_private_key):
    """Create JWT signer instance"""
    return JwtSignatureProvider(private_key=test_private_key)


@pytest_asyncio.fixture(scope="function")
async def test_services(repository, jwt_signer):
    """Create Services instance for testing"""
    services = Services()
    services.jwt_signer = jwt_signer
    services.repository = repository
    return services


@pytest_asyncio.fixture(scope="function")
async def test_app(test_services):
    @asynccontextmanager
    async def test_lifespan(_app: FastAPI):
        yield

    app = FastAPI(lifespan=test_lifespan)

    # Import routes
    from source.routes import auth, root
    app.include_router(root.router)
    app.include_router(auth.router)

    # Override dependencies
    from source.depends.repository import get_repository
    from source.depends.jwt_signer import get_jwt_signer
    from source.depends.app import get_services

    app.dependency_overrides[get_services] = lambda: test_services
    app.dependency_overrides[get_repository] = lambda: test_services.repository
    app.dependency_overrides[get_jwt_signer] = lambda: test_services.jwt_signer

    yield app

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(test_app):
    """Create HTTP client for testing"""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        yield ac


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "tax_id": "12345678900",
        "email": "test@example.com",
        "name": "Test User"
    }
