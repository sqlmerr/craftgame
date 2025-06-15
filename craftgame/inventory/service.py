from dataclasses import dataclass
from uuid import UUID

from craftgame.common.exceptions import NotFound
from craftgame.inventory.dto import InventoryItemDTO, CreateInventoryItemDTO
from craftgame.inventory.exceptions import InventoryItemAlreadyExists
from craftgame.inventory.interfaces.deleter import InventoryDeleter
from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.inventory.interfaces.repo import InventoryRepo
from craftgame.inventory.interfaces.writer import InventoryWriter
from craftgame.inventory.model import InventoryItem
from craftgame.item.interfaces.repo import ItemRepo
from craftgame.item.model import Item


@dataclass(frozen=True)
class InventoryService(InventoryReader, InventoryWriter, InventoryDeleter):
    repo: InventoryRepo
    item_repo: ItemRepo

    async def get_inventory_item_by_id(self, inventory_id: UUID) -> InventoryItemDTO | None:
        inv = await self.repo.find_one_inventory_item_filtered(InventoryItem.id == inventory_id)
        if not inv:
            return None
        return InventoryItemDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id, count=inv.count)

    async def get_inventory_item_by_item_id_and_user_id(
        self, item_id: UUID, user_id: UUID
    ) -> InventoryItemDTO | None:
        inv = await self.repo.find_one_inventory_item_filtered(
            (InventoryItem.item_id == item_id) & (InventoryItem.user_id == user_id)
        )
        if not inv:
            return None
        return InventoryItemDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id, count=inv.count)

    async def get_all_inventory_items_by_user(
        self, user_id: UUID
    ) -> list[InventoryItemDTO]:
        inventories = await self.repo.find_all_inventory_items(InventoryItem.user_id == user_id)
        dtos = []
        for inv in inventories:
            dtos.append(
                InventoryItemDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id, count=inv.count)
            )
        return dtos

    async def add_inventory_item(self, data: CreateInventoryItemDTO) -> InventoryItemDTO:
        inv = await self.repo.find_one_inventory_item_filtered(
            (InventoryItem.user_id == data.user_id) & (InventoryItem.item_id == data.item_id)
        )
        if inv:
            await self.repo.update_inventory_item(inv.id, {"count": inv.count + data.count})
            return await self.get_inventory_item_by_id(inv.id)

        item = await self.item_repo.find_one_item_filtered(Item.id == data.item_id)
        if not item:
            raise NotFound

        inventory_id = await self.repo.create_inventory_item(data.__dict__)
        return await self.get_inventory_item_by_id(inventory_id)

    async def delete_inventory_item(self, inventory_id: UUID) -> None:
        await self.repo.delete_inventory_item(inventory_id)
