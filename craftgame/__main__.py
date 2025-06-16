import logging

import uvicorn

from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from craftgame.config import Settings
from craftgame.di import init_di
from craftgame.dto.item import CreateItemDTO
from craftgame.logging import configure_logging
from craftgame.models.item import Item
from craftgame.core.services.item import ItemService
from craftgame.api import create_app
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.aiogram import setup_dishka as setup_aiogram_dishka

from craftgame.bot import init_bot, init_dispatcher


logger = logging.getLogger(__name__)


def init_db(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.postgres.dsn())
    session_maker = async_sessionmaker(bind=engine)
    return session_maker


async def create_initial_data(item_service: ItemService):
    logger.debug("Applying initial data")
    for name, emoji in [
        ("water", "💧"),
        ("fire", "🔥"),
        ("wind", "💨"),
        ("earth", "🌎"),
    ]:
        item = await item_service.repo.find_one_item_filtered(Item.name == name)
        if item:
            continue
        await item_service.create_item(CreateItemDTO(name, emoji, opened_by_id=None))
    logger.debug("Applied!")


def main() -> FastAPI:
    settings = Settings()
    configure_logging(settings)
    logger.info(f"Using {settings.environment} environment")
    session_maker = init_db(settings)
    container = init_di(settings, session_maker)

    bot = init_bot(settings)
    dp = init_dispatcher()
    setup_aiogram_dishka(container, dp, auto_inject=True)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Starting application")
        async with container() as c:
            await create_initial_data(await c.get(ItemService))

        logger.debug("Initializing webhook")
        await bot.set_webhook(
            url=f"{settings.webhook_url}webhook",
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logger.debug("Success")
        await dp.startup.trigger(bot=bot)

        logger.info(f"Craftgame is running on {settings.host}:{settings.port}")
        yield
        await dp.shutdown.trigger()
        await bot.session.close()
        await app.state.dishka_container.close()
        logger.info("Goodbye")

    app = create_app(lifespan=lifespan)
    setup_dishka(container, app)

    @app.post("/webhook")
    async def webhook(request: Request) -> None:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)

    uvicorn.run(
        app, host=settings.host, port=settings.port, use_colors=False, log_level="error"
    )


if __name__ == "__main__":
    main()
