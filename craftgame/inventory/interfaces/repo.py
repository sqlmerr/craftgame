from typing import Protocol, Any
from uuid import UUID

from sqlalchemy import ColumnElement

from craftgame.inventory.model import InventoryItem


class InventoryRepo(Protocol):
    async def create_inventory_item(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_inventory_item_filtered(
        self, filters: ColumnElement[bool]
    ) -> InventoryItem | None:
        raise NotImplementedError

    async def find_all_inventory_items(
        self, filters: ColumnElement[bool]
    ) -> list[InventoryItem]:
        raise NotImplementedError

    async def update_inventory_item(self, inventory_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_inventory_item(self, inventory_id: UUID) -> None:
        raise NotImplementedError
