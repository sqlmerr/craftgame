from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.item.interfaces import ItemReader
from craftgame.presentation.bot.keyboards import inventory_keyboard
from craftgame.user.dto import UserDTO

router = Router()


@router.callback_query(F.data == "open_inventory")
async def inventory_menu(
    call: CallbackQuery,
    user: UserDTO,
    inventory_reader: FromDishka[InventoryReader],
    item_reader: FromDishka[ItemReader],
):
    await call.answer()
    inventory = await inventory_reader.get_all_inventory_items_by_user(user.id)
    items = []
    for i in inventory:
        item = await item_reader.get_item_by_id(i.item_id)
        items.append(item)

    reply_markup = inventory_keyboard(items)
    await call.message.edit_text("<i>Inventory:</i>", reply_markup=reply_markup)
