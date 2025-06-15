from typing import Protocol
from uuid import UUID

from craftgame.dto.item import ItemDTO


class ItemReader(Protocol):
    async def get_item_by_id(self, item_id: UUID) -> ItemDTO | None:
        raise NotImplementedError

    async def get_item_by_name(self, item_name: str) -> ItemDTO | None:
        raise NotImplementedError

    async def get_all_items_opened_by_user(self, user_id: UUID) -> list[ItemDTO]:
        raise NotImplementedError
