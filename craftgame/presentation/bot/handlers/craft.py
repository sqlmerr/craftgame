from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka

from craftgame.ai.dto import GenerateItemDTO
from craftgame.ai.interfaces.item_generator import ItemGenerator
from craftgame.common.exceptions import NotFound
from craftgame.craft.dto import CreateCraftDTO
from craftgame.craft.service import CraftService
from craftgame.inventory.dto import CreateInventoryDTO
from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.inventory.service import InventoryService
from craftgame.item.dto import CreateItemDTO
from craftgame.item.interfaces import ItemReader
from craftgame.item.service import ItemService
from craftgame.presentation.bot.calldata import (
    ChooseIngredientData,
    IngredientSelectData,
    CraftResultData,
)
from craftgame.presentation.bot.keyboards import (
    choose_ingredients_keyboard,
    ingredients_keyboard,
)
from craftgame.presentation.bot.states import CraftMenuState
from craftgame.util import normalize_snake_case
from craftgame.user.dto import UserDTO

router = Router()


@router.callback_query(F.data == "open_craft_menu")
async def open_craft_menu(
    call: CallbackQuery,
    state: FSMContext,
    item_reader: FromDishka[ItemReader],
):
    await call.answer()
    if await state.get_state() != CraftMenuState.main:
        await state.set_state(CraftMenuState.main)
        await state.set_data({"ingredient1": None, "ingredient2": None})
    data = await state.get_data()
    ingredient1 = await item_reader.get_item_by_id(data.get("ingredient1"))
    ingredient2 = await item_reader.get_item_by_id(data.get("ingredient2"))

    await call.message.edit_text(
        text="<i>Select items to craft from</i>",
        reply_markup=choose_ingredients_keyboard(ingredient1, ingredient2),
    )


@router.callback_query(CraftMenuState.main, ChooseIngredientData.filter())
async def choose_ingredients(
    call: CallbackQuery,
    user: UserDTO,
    callback_data: ChooseIngredientData,
    inventory_reader: FromDishka[InventoryReader],
    item_reader: FromDishka[ItemReader],
):
    await call.answer()
    inventory = await inventory_reader.get_all_inventory_items_by_user(user.id)
    items = []
    for i in inventory:
        item = await item_reader.get_item_by_id(i.item_id)
        items.append(item)

    keyboard = ingredients_keyboard(place=callback_data.place, items=items)
    await call.message.edit_text("Select ingredient", reply_markup=keyboard)


@router.callback_query(CraftMenuState.main, IngredientSelectData.filter())
async def select_ingredient(
    call: CallbackQuery,
    state: FSMContext,
    callback_data: IngredientSelectData,
    item_reader: FromDishka[ItemReader],
):
    await call.answer()

    await state.update_data(
        {
            f"ingredient{callback_data.place if callback_data.place == 1 else 2}":
                callback_data.ingredient_id
        }
    )
    data = await state.get_data()

    ingredient1 = await item_reader.get_item_by_id(data.get("ingredient1"))
    ingredient2 = await item_reader.get_item_by_id(data.get("ingredient2"))

    keyboard = choose_ingredients_keyboard(ingredient1, ingredient2)
    await call.message.edit_text(
        "Select items to craft from", reply_markup=keyboard
    )


@router.callback_query(CraftMenuState.main, CraftResultData.filter())
async def craft_result(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    item_service: FromDishka[ItemService],
    item_generator: FromDishka[ItemGenerator],
    craft_service: FromDishka[CraftService],
    inventory_service: FromDishka[InventoryService],
):
    await call.answer("loading")
    data = await state.get_data()
    new_item_in_inventory = False
    discovered_new_item = False

    craft = await craft_service.repo.find_one_craft_by_ingredients(
        data["ingredient1"], data["ingredient2"]
    )
    if not craft:
        ingr1 = await item_service.get_item_by_id(data["ingredient1"])
        ingr2 = await item_service.get_item_by_id(data["ingredient2"])
        generated_item = await item_generator.generate_item(
            GenerateItemDTO(ingredient1_name=ingr1.name, ingredient2_name=ingr2.name)
        )
        if not (item := await item_service.get_item_by_name(generated_item.name)):
            discovered_new_item = True
            item = await item_service.create_item(
                CreateItemDTO(
                    name=generated_item.name,
                    emoji=generated_item.emoji,
                    opened_by_id=user.id,
                )
            )

        try:
            craft = await craft_service.get_item_craft(item.id)
        except NotFound:
            craft = None
        if not craft:
            craft = await craft_service.create_craft(
                CreateCraftDTO(result_item_id=item.id, ingredients_ids=[ingr1.id, ingr2.id])
            )
        item_in_inventory = (
            await inventory_service.get_inventory_by_item_id_and_user_id(
                craft.result_item_id, user_id=user.id
            )
        )
        if not item_in_inventory:
            new_item_in_inventory = True
            await inventory_service.create_inventory(
                CreateInventoryDTO(user_id=user.id, item_id=craft.result_item_id)
            )
    else:
        item_in_inventory = (
            await inventory_service.get_inventory_by_item_id_and_user_id(
                craft.result_item_id, user_id=user.id
            )
        )
        if not item_in_inventory:
            new_item_in_inventory = True
            await inventory_service.create_inventory(
                CreateInventoryDTO(user_id=user.id, item_id=craft.result_item_id)
            )
        item = await item_service.get_item_by_id(craft.result_item_id)

    await state.clear()
    await call.message.edit_text(
        text=(
            f"<b>You crafted item</b> <code>{item.emoji} {normalize_snake_case(item.name)}</code>!\n"
            + (
                "Congratulations, you've discovered new item!\n"
                if discovered_new_item
                else ""
            )
            + ("It's new item in your inventory!" if new_item_in_inventory else "")
        )
    )
