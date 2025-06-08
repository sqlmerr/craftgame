import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import Container, FromDishka
from dishka.integrations.aiogram import inject

from craftgame.config import Settings
from craftgame.user.dto import CreateUserDTO
from craftgame.user.exceptions import UserWithThisTelegramIdAlreadyExists
from craftgame.user.service import UserService


router = Router()


@router.message(CommandStart())
@inject
async def handler(message: Message, user_service: FromDishka[UserService]):
    with suppress(UserWithThisTelegramIdAlreadyExists):
        await user_service.create_user(CreateUserDTO(tg_id=message.from_user.id))
        logging.info(f"created user with id {message.from_user.id}")

    await message.answer(f"Hello, <i>{message.from_user.first_name}</i>")


def init_bot(settings: Settings) -> Bot:
    return Bot(
        settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


def init_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)

    return dp
