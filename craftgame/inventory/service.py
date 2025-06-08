from dataclasses import dataclass
from uuid import UUID

from craftgame.common.exceptions import NotFound
from craftgame.inventory.dto import InventoryDTO, CreateInventoryDTO
from craftgame.inventory.exceptions import InventoryAlreadyExists
from craftgame.inventory.interfaces.deleter import InventoryDeleter
from craftgame.inventory.interfaces.reader import InventoryReader
from craftgame.inventory.interfaces.repo import InventoryRepo
from craftgame.inventory.interfaces.writer import InventoryWriter
from craftgame.inventory.model import Inventory
from craftgame.item.interfaces.repo import ItemRepo
from craftgame.item.model import Item


@dataclass(frozen=True)
class InventoryService(InventoryReader, InventoryWriter, InventoryDeleter):
    repo: InventoryRepo
    item_repo: ItemRepo

    async def get_inventory_by_id(self, inventory_id: UUID) -> InventoryDTO | None:
        inv = await self.repo.find_one_inventory_filtered(Inventory.id == inventory_id)
        if not inv:
            return None
        return InventoryDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id)

    async def get_inventory_by_item_id_and_user_id(
        self, item_id: UUID, user_id: UUID
    ) -> InventoryDTO | None:
        inv = await self.repo.find_one_inventory_filtered(
            (Inventory.item_id == item_id) & (Inventory.user_id == user_id)
        )
        if not inv:
            return None
        return InventoryDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id)

    async def get_all_inventory_items_by_user(
        self, user_id: UUID
    ) -> list[InventoryDTO]:
        inventories = await self.repo.find_all_inventories(Inventory.user_id == user_id)
        dtos = []
        for inv in inventories:
            dtos.append(
                InventoryDTO(id=inv.id, user_id=inv.user_id, item_id=inv.item_id)
            )
        return dtos

    async def create_inventory(self, data: CreateInventoryDTO) -> InventoryDTO:
        inv = await self.repo.find_one_inventory_filtered(
            (Inventory.user_id == data.user_id) & (Inventory.item_id == data.item_id)
        )
        if inv:
            raise InventoryAlreadyExists

        item = await self.item_repo.find_one_item_filtered(Item.id == data.item_id)
        if not item:
            raise NotFound

        inventory_id = await self.repo.create_inventory(data.__dict__)
        return await self.get_inventory_by_id(inventory_id)

    async def delete_inventory(self, inventory_id: UUID) -> None:
        await self.repo.delete_inventory(inventory_id)
