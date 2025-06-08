from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class OpenItemData(CallbackData, prefix="item"):
    item_id: UUID


class ChooseIngredientData(CallbackData, prefix="choose_ingredient"):
    place: int  # 1 or 2


class CraftResultData(CallbackData, prefix="craft_result"):
    pass


class IngredientSelectData(CallbackData, prefix="ingredient_select"):
    ingredient_id: UUID
    place: int  # 1 or 2
