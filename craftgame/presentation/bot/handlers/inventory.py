from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka import FromDishka

from craftgame.common.exceptions import NotFound
from craftgame.craft.interfaces.reader import CraftReader
from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.item.interfaces import ItemReader
from craftgame.presentation.bot.calldata import OpenItemData
from craftgame.presentation.bot.keyboards import inventory_keyboard
from craftgame.util import normalize_snake_case
from craftgame.user.dto import UserDTO

router = Router()


@router.callback_query(F.data == "open_inventory")
@router.message(Command("inventory"))
async def inventory_menu(
    event: CallbackQuery | Message,
    user: UserDTO,
    inventory_reader: FromDishka[InventoryReader],
    item_reader: FromDishka[ItemReader],
):
    inventory = await inventory_reader.get_all_inventory_items_by_user(user.id)
    items = []
    for i in inventory:
        item = await item_reader.get_item_by_id(i.item_id)
        items.append((item, i.count))

    reply_markup = inventory_keyboard(items)
    if isinstance(event, CallbackQuery):
        await event.message.edit_text("Inventory:", reply_markup=reply_markup)
    else:
        await event.reply("Inventory:", reply_markup=reply_markup)


@router.callback_query(OpenItemData.filter())
async def item_info_menu(
        call: CallbackQuery,
        user: UserDTO,
        callback_data: OpenItemData,
        inventory_reader: FromDishka[InventoryReader],
        item_reader: FromDishka[ItemReader],
        craft_reader: FromDishka[CraftReader],
):
    await call.answer()
    inv = await inventory_reader.get_inventory_item_by_item_id_and_user_id(item_id=callback_data.item_id, user_id=user.id)
    if not inv:
        return

    item = await item_reader.get_item_by_id(inv.item_id)
    if not item:
        return

    try:
        craft = await craft_reader.get_item_craft(item.id)
    except NotFound:
        craft = None
    ingredient1 = None
    ingredient2 = None
    if craft:
        ingredient1 = await item_reader.get_item_by_id(craft.ingredients_ids[0])
        ingredient2 = await item_reader.get_item_by_id(craft.ingredients_ids[1])

    text = f"{inv.count} Item <code>{item.emoji} {normalize_snake_case(item.name)}</code>\n"
    text += "<i>Opened by you</i>\n" if item.opened_by_id == user.id else ""
    text += f"<blockquote><i>Crafted from:</i>\n<code>{ingredient1.item_name}</code> + <code>{ingredient2.item_name}</code></blockquote>" if craft else ""

    reply_markup = InlineKeyboardBuilder().button(text="← back", callback_data="open_inventory").as_markup()

    await call.message.edit_text(text, reply_markup=reply_markup)