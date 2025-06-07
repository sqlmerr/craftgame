from typing import Protocol
from uuid import UUID

from ..dto import CraftDTO


class CraftReader(Protocol):
    async def get_craft_by_id(self, craft_id: UUID) -> CraftDTO | None:
        raise NotImplementedError

    async def get_item_crafts(self, item_id: UUID) -> list[CraftDTO]:
        raise NotImplementedError
