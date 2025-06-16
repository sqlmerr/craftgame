from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from craftgame.config import Settings
from craftgame.bot.handlers import init_routers
from craftgame.bot.middlewares.user import UserMiddleware


def init_bot(settings: Settings) -> Bot:
    return Bot(
        settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


async def on_start(bot: Bot):
    commands = [
        BotCommand(command="start", description="Restart bot"),
        BotCommand(command="inventory", description="Open your inventory"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


def init_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())
    dp.startup.register(on_start)

    dp.include_router(init_routers())

    return dp
