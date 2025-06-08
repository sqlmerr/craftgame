from typing import AsyncGenerator

import sqlalchemy.exc
from dishka import Provider, provide, AnyOf, Scope, AsyncContainer, make_async_container
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from craftgame.ai.interfaces.item_generator import ItemGenerator
from craftgame.ai.service import AiService
from craftgame.config import Settings
from craftgame.craft.interfaces.deleter import CraftDeleter
from craftgame.craft.interfaces.reader import CraftReader
from craftgame.craft.interfaces.repo import CraftRepo
from craftgame.craft.interfaces.writer import CraftWriter
from craftgame.craft.repository import CraftRepository
from craftgame.craft.service import CraftService
from craftgame.inventory.interfaces.deleter import InventoryDeleter
from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.inventory.interfaces.repo import InventoryRepo
from craftgame.inventory.interfaces.writer import InventoryWriter
from craftgame.inventory.repository import InventoryRepository
from craftgame.inventory.service import InventoryService
from craftgame.item.interfaces.deleter import ItemDeleter
from craftgame.item.interfaces.reader import ItemReader
from craftgame.item.interfaces.repo import ItemRepo
from craftgame.item.interfaces.writer import ItemWriter
from craftgame.item.repository import ItemRepository
from craftgame.item.service import ItemService
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
