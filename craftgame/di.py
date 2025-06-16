from typing import AsyncGenerator

import sqlalchemy.exc
from dishka import Provider, provide, AnyOf, Scope, AsyncContainer, make_async_container
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from craftgame.core.interfaces.ai.item_generator import ItemGenerator
from craftgame.core.services.ai import AiService
from craftgame.config import Settings
from craftgame.core.interfaces.craft.deleter import CraftDeleter
from craftgame.core.interfaces.craft.reader import CraftReader
from craftgame.core.interfaces.craft.repo import CraftRepo
from craftgame.core.interfaces.craft.writer import CraftWriter
from craftgame.database.repositories.craft import CraftRepository
from craftgame.core.services.craft import CraftService
from craftgame.core.interfaces.inventory.deleter import InventoryDeleter
from craftgame.core.interfaces.inventory.reader import InventoryReader
from craftgame.core.interfaces.inventory.repo import InventoryRepo
from craftgame.core.interfaces.inventory.writer import InventoryWriter
from craftgame.database.repositories.inventory import InventoryRepository
from craftgame.core.services.inventory import InventoryService
from craftgame.core.interfaces.item.deleter import ItemDeleter
from craftgame.core.interfaces.item.reader import ItemReader
from craftgame.core.interfaces.item.repo import ItemRepo
from craftgame.core.interfaces.item.writer import ItemWriter
from craftgame.database.repositories.item import ItemRepository
from craftgame.core.services.item import ItemService
from craftgame.core.interfaces.user import (
    UserReader,
    UserWriter,
    UserUpdater,
    UserDeleter,
)
from craftgame.core.interfaces.user.repo import UserRepo
from craftgame.database.repositories.user import UserRepository
from craftgame.core.services.user import UserService


class DatabaseProvider(Provider):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__()
        self.session_maker = session_maker

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_maker() as session:
            try:
                yield session
            except sqlalchemy.exc.SQLAlchemyError:
                await session.rollback()
            finally:
                await session.commit()


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: AsyncSession) -> UserRepo:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_item_repo(self, session: AsyncSession) -> ItemRepo:
        return ItemRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_craft_repo(self, session: AsyncSession) -> CraftRepo:
        return CraftRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_inventory_repo(self, session: AsyncSession) -> InventoryRepo:
        return InventoryRepository(session)


class ServiceProvider(Provider):
    @provide(
        scope=Scope.REQUEST,
        provides=AnyOf[UserService, UserWriter, UserReader, UserDeleter, UserUpdater],
    )
    def get_user_service(
        self, repo: UserRepo, inv_repo: InventoryRepo, item_repo: ItemRepo
    ):
        return UserService(repo, inv_repo, item_repo)

    @provide(
        scope=Scope.REQUEST,
        provides=AnyOf[ItemReader, ItemWriter, ItemDeleter, ItemService],
    )
    def get_item_service(self, repo: ItemRepo):
        return ItemService(repo)

    @provide(
        scope=Scope.REQUEST,
        provides=AnyOf[CraftReader, CraftWriter, CraftDeleter, CraftService],
    )
    def get_craft_service(self, repo: CraftRepo):
        return CraftService(repo)

    @provide(
        scope=Scope.REQUEST,
        provides=AnyOf[
            InventoryReader, InventoryWriter, InventoryDeleter, InventoryService
        ],
    )
    def get_inventory_service(self, repo: InventoryRepo, item_repo: ItemRepo):
        return InventoryService(repo, item_repo)

    @provide(scope=Scope.REQUEST, provides=AnyOf[ItemGenerator, AiService])
    def get_ai_service(self, settings: Settings):
        ai_client = AsyncOpenAI(
            api_key=settings.ai_token, base_url="https://openrouter.ai/api/v1"
        )

        return AiService(ai_client)


class ConfigProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return self.settings


def init_di(
    config: Settings, session_maker: async_sessionmaker[AsyncSession]
) -> AsyncContainer:
    container = make_async_container(
        DatabaseProvider(session_maker),
        RepositoryProvider(),
        ServiceProvider(),
        ConfigProvider(config),
    )

    return container
