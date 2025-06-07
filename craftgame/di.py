from typing import AsyncGenerator

from dishka import Provider, provide, AnyOf, Scope, AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from craftgame.config import Settings
from craftgame.user.interfaces import UserReader, UserWriter, UserUpdater, UserDeleter
from craftgame.user.interfaces.repo import UserRepo
from craftgame.user.repository import UserRepository
from craftgame.user.service import UserService


class DatabaseProvider(Provider):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__()
        self.session_maker = session_maker

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_maker() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: AsyncSession) -> UserRepo:
        return UserRepository(session)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self, repo: UserRepo) -> AnyOf[UserService, UserReader, UserWriter, UserUpdater, UserDeleter]:
        return UserService(repo)


class ConfigProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return self.settings


async def init_di(config: Settings, session_maker: async_sessionmaker[AsyncSession]) -> AsyncContainer:
    container = make_async_container(
        DatabaseProvider(session_maker),
        RepositoryProvider(),
        ServiceProvider(),
        ConfigProvider(config)
    )

    return container

