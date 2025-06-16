from typing import Protocol
from uuid import UUID

from craftgame.dto.inventory import CreateInventoryItemDTO, InventoryItemDTO


class InventoryWriter(Protocol):
    async def add_inventory_item(
        self, data: CreateInventoryItemDTO
    ) -> InventoryItemDTO:
        raise NotImplementedError

    async def set_inventory_item_count(self, inventory_item_id: UUID, count: int):
        raise NotImplementedError