from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from craftgame.item.dto import ItemDTO
from craftgame.presentation.bot.calldata import (
    OpenItemData,
    ChooseIngredientData,
    CraftResultData,
    IngredientSelectData,
)
from craftgame.util import normalize_snake_case


def main_menu_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="Craft", callback_data="open_craft_menu")
    b.button(text="Inventory", callback_data="open_inventory")
    b.adjust(2)

    return b.as_markup()


def inventory_keyboard(items: list[ItemDTO]):
    b = InlineKeyboardBuilder()
    for i in items:
        b.button(
            text=f"{i.emoji} {normalize_snake_case(i.name)}",
            callback_data=OpenItemData(item_id=i.id).pack(),
        )
    b.adjust(3)

    b.row(InlineKeyboardButton(text="← back", callback_data="open_main_menu"))

    return b.as_markup()


def choose_ingredients_keyboard(
    ingredient1: ItemDTO | None = None, ingredient2: ItemDTO | None = None
):
    b = InlineKeyboardBuilder()
    if ingredient1:
        b.button(
            text=f"{ingredient1.emoji} {normalize_snake_case(ingredient1.name)}",
            callback_data=ChooseIngredientData(place=1).pack(),
        )
    else:
        b.button(text="+", callback_data=ChooseIngredientData(place=1))

    if ingredient2:
        b.button(
            text=f"{ingredient2.emoji} {normalize_snake_case(ingredient2.name)}",
            callback_data=ChooseIngredientData(place=2).pack(),
        )
    else:
        b.button(text="+", callback_data=ChooseIngredientData(place=2))

    if ingredient1 and ingredient2:
        b.button(text="Craft", callback_data=CraftResultData())

    b.button(text="← back", callback_data="open_main_menu")
    b.adjust(1)

    return b.as_markup()


def ingredients_keyboard(place: int, items: list[ItemDTO]):
    b = InlineKeyboardBuilder()
    for i in items:
        b.button(
            text=f"{i.emoji} {normalize_snake_case(i.name)}",
            callback_data=IngredientSelectData(ingredient_id=i.id, place=place),
        )
    b.adjust(3)

    b.row(InlineKeyboardButton(text="← back", callback_data="open_craft_menu"))

    return b.as_markup()
