from typing import Protocol
from uuid import UUID


class InventoryDeleter(Protocol):
    async def delete_inventory_item(self, inventory_id: UUID) -> None:
        raise NotImplementedError
