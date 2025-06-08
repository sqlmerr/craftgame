from typing import Protocol

from ..dto import CreateInventoryDTO, InventoryDTO


class InventoryWriter(Protocol):
    async def create_inventory(self, data: CreateInventoryDTO) -> InventoryDTO:
        raise NotImplementedError
