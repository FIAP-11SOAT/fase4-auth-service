from source.configs.secrets import Secrets
from source.configs.settings import Settings
from source.helpers.jwt import JwtSignatureProvider
from source.helpers.repository import AsyncDatabaseRepository


class Services:
    jwt_signer: JwtSignatureProvider = None
    repository: AsyncDatabaseRepository = None

    @classmethod
    def new(cls, settings: Settings, secrets: Secrets):
        instance = cls()
        instance.jwt_signer = JwtSignatureProvider(private_key=secrets.jwt_private_key)
        instance.repository = AsyncDatabaseRepository(table_name=settings.application_table_name)
        return instance
