from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from craftgame.config import Settings
from craftgame.presentation.bot.handlers import init_routers
from craftgame.presentation.bot.middlewares.user import UserMiddleware


def init_bot(settings: Settings) -> Bot:
    return Bot(
        settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


def init_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())

    dp.include_router(init_routers())

    return dp
