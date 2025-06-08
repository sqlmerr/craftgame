from typing import Protocol
from uuid import UUID

from ..dto import InventoryDTO


class InventoryReader(Protocol):
    async def get_inventory_by_id(self, inventory_id: UUID) -> InventoryDTO | None:
        raise NotImplementedError

    async def get_inventory_by_item_id_and_user_id(
        self, item_id: UUID, user_id: UUID
    ) -> InventoryDTO | None:
        raise NotImplementedError

    async def get_all_inventory_items_by_user(
        self, user_id: UUID
    ) -> list[InventoryDTO]:
        raise NotImplementedError
