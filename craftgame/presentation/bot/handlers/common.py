from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from craftgame.presentation.bot.keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "open_main_menu")
async def start_cmd(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.reply_sticker(
            "CAACAgUAAxkBAAEOqihoRXbKM7GnHSpAdtmBYWht_9KetwAC0AEAAt8fchkuFenDj8oThzYE"
        )
        await event.answer("<i>Main menu</i>", reply_markup=main_menu_keyboard())
    else:
        await event.message.edit_text(
            "<i>Main menu</i>", reply_markup=main_menu_keyboard()
        )
