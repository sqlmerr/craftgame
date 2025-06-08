from dataclasses import dataclass
from uuid import UUID

from craftgame.item.dto import ItemDTO, CreateItemDTO
from craftgame.item.interfaces.deleter import ItemDeleter
from craftgame.item.interfaces.reader import ItemReader
from craftgame.item.interfaces.repo import ItemRepo
from craftgame.item.interfaces.writer import ItemWriter
from craftgame.item.model import Item


@dataclass(frozen=True)
class ItemService(ItemReader, ItemWriter, ItemDeleter):
    repo: ItemRepo

    async def get_item_by_id(self, item_id: UUID) -> ItemDTO | None:
        item = await self.repo.find_one_item_filtered(Item.id == item_id)
        if not item:
            return None
        return ItemDTO(
            id=item.id,
            name=item.name,
            emoji=item.emoji,
            opened_by_id=item.opened_by_id,
            opened_at=item.opened_at,
        )

    async def get_item_by_name(self, item_name: str) -> ItemDTO | None:
        item = await self.repo.find_one_item_filtered(Item.name == item_name)
        if not item:
            return None
        return ItemDTO(
            id=item.id,
            name=item.name,
            emoji=item.emoji,
            opened_by_id=item.opened_by_id,
            opened_at=item.opened_at,
        )

    async def get_all_items_opened_by_user(self, user_id: UUID) -> list[ItemDTO]:
        items = await self.repo.find_all_items(Item.opened_by_id == user_id)
        dtos = []
        for i in items:
            dtos.append(
                ItemDTO(
                    id=i.id,
                    name=i.name,
                    emoji=i.emoji,
                    opened_by_id=i.opened_by_id,
                    opened_at=i.opened_at,
                )
            )
        return dtos

    async def create_item(self, data: CreateItemDTO) -> ItemDTO:
        item_id = await self.repo.create_item(data.__dict__)
        return await self.get_item_by_id(item_id)

    async def delete_item(self, item_id: UUID) -> None:
        await self.repo.delete_item(item_id)
