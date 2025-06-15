from typing import Protocol
from uuid import UUID

from craftgame.dto.inventory import InventoryItemDTO


class InventoryReader(Protocol):
    async def get_inventory_item_by_id(self, inventory_id: UUID) -> InventoryItemDTO | None:
        raise NotImplementedError

    async def get_inventory_item_by_item_id_and_user_id(
        self, item_id: UUID, user_id: UUID
    ) -> InventoryItemDTO | None:
        raise NotImplementedError

    async def get_all_inventory_items_by_user(
        self, user_id: UUID
    ) -> list[InventoryItemDTO]:
        raise NotImplementedError
