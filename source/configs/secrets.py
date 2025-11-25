from dataclasses import dataclass

from source.configs.settings import Settings
from source.helpers.aws import get_aws_secrets


@dataclass
class Secrets:
    jwt_private_key: str

    @classmethod
    async def new(cls, settings: Settings):
        secrets = await get_aws_secrets(settings.application_secret_name)
        return cls(
            jwt_private_key=secrets["JWT_PRIVATE_KEY"],
        )
