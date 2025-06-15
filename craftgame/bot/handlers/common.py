import random

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from craftgame.bot.keyboards import main_menu_keyboard
from craftgame.bot.constants import STICKERS

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "open_main_menu")
async def start_cmd(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.reply_sticker(
            random.choice(STICKERS["welcome"]),
        )
        await event.answer("<i>Main menu</i>", reply_markup=main_menu_keyboard())
    else:
        await event.message.edit_text(
            "Main menu", reply_markup=main_menu_keyboard()
        )
