from typing import Protocol, Any
from uuid import UUID

from sqlalchemy import ColumnElement

from craftgame.models.craft import Craft


class CraftRepo(Protocol):
    async def create_craft(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_craft_filtered(
        self, filters: ColumnElement[bool]
    ) -> Craft | None:
        raise NotImplementedError

    async def find_one_craft_by_ingredients(
        self, ingredient1_id: UUID, ingredient2_id: UUID
    ) -> Craft | None:
        raise NotImplementedError

    async def find_all_crafts(self, filters: ColumnElement[bool]) -> list[Craft]:
        raise NotImplementedError

    async def update_craft(self, craft_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_craft(self, craft_id: UUID) -> None:
        raise NotImplementedError
