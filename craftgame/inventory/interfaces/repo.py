from typing import Protocol, Any
from uuid import UUID

from sqlalchemy import ColumnElement

from craftgame.inventory.model import Inventory


class InventoryRepo(Protocol):
    async def create_inventory(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_inventory_filtered(
        self, filters: ColumnElement[bool]
    ) -> Inventory | None:
        raise NotImplementedError

    async def find_all_inventories(
        self, filters: ColumnElement[bool]
    ) -> list[Inventory]:
        raise NotImplementedError

    async def update_inventory(self, inventory_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_inventory(self, inventory_id: UUID) -> None:
        raise NotImplementedError
