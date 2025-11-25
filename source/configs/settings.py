from pydantic.v1 import BaseSettings

from source.__version__ import __version__


class Settings(BaseSettings):
    profile: str = "development"
    short_profile: str = "dev"
    version: str = __version__
    application_name: str = "fase4-auth-service"
    application_secret_name: str = "fase4-auth-service-secrets"
    application_table_name: str = "fase4-auth-service-users"

    __map_profile_to_short__ = {
        "development": "dev",
        "staging": "stg",
        "production": "prod",
    }

    @classmethod
    def new(cls):
        instance = cls()
        if instance.profile not in cls.__map_profile_to_short__:
            raise ValueError(
                f"Invalid profile '{instance.profile}'. "
                f"Must be one of: {list(cls.__map_profile_to_short__.keys())}"
            )
        instance.short_profile = cls.__map_profile_to_short__[instance.profile]
        return instance
