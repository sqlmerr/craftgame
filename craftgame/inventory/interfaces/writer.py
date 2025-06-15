from typing import Protocol

from ..dto import CreateInventoryItemDTO, InventoryItemDTO


class InventoryWriter(Protocol):
    async def add_inventory_item(self, data: CreateInventoryItemDTO) -> InventoryItemDTO:
        raise NotImplementedError
