from typing import Protocol

from craftgame.dto.inventory import CreateInventoryItemDTO, InventoryItemDTO


class InventoryWriter(Protocol):
    async def add_inventory_item(self, data: CreateInventoryItemDTO) -> InventoryItemDTO:
        raise NotImplementedError
