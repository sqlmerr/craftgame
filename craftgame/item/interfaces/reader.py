from typing import Protocol
from uuid import UUID

from ..dto import ItemDTO


class ItemReader(Protocol):
    async def get_user_by_id(self, item_id: UUID) -> ItemDTO | None:
        raise NotImplementedError
