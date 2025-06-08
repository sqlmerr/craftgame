from typing import Protocol
from uuid import UUID


class InventoryDeleter(Protocol):
    async def delete_inventory(self, inventory_id: UUID) -> None:
        raise NotImplementedError
