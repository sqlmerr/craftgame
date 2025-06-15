from typing import Protocol
from uuid import UUID

from craftgame.dto.craft import CraftDTO


class CraftReader(Protocol):
    async def get_craft_by_id(self, craft_id: UUID) -> CraftDTO | None:
        raise NotImplementedError

    async def get_item_craft(self, item_id: UUID) -> CraftDTO:
        raise NotImplementedError
