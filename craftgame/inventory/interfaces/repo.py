from typing import Protocol, Any
from uuid import UUID

from craftgame.inventory.model import Inventory


class InventoryRepo(Protocol):
    async def create_inventory(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_inventory_filtered(
        self, filters: dict[str, Any]
    ) -> Inventory | None:
        raise NotImplementedError

    async def find_all_inventories(self, filters: dict[str, Any]) -> list[Inventory]:
        raise NotImplementedError

    async def update_inventory(self, inventory_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_inventory(self, inventory_id: UUID) -> None:
        raise NotImplementedError
