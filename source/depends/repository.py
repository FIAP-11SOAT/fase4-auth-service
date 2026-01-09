from typing import Annotated

from fastapi import Depends
from typing_extensions import TypeAlias

from source.depends.app import DependsServices
from source.helpers.repository import AsyncDatabaseRepository


def get_repository(services: DependsServices):
    if not services.repository:
        raise RuntimeError('Repository has not been initialized in app.lifespan')
    return services.repository


DependsRepository: TypeAlias = Annotated[AsyncDatabaseRepository, Depends(get_repository)]
