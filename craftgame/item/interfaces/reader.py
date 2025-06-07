from typing import Protocol
from uuid import UUID

from ..dto import ItemDTO


class ItemReader(Protocol):
    async def get_item_by_id(self, item_id: UUID) -> ItemDTO | None:
        raise NotImplementedError

    async def get_all_items_opened_by_user(self, user_id: UUID) -> list[ItemDTO]:
        raise NotImplementedError
