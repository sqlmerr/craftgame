from typing import Protocol

from craftgame.dto.craft import CreateCraftDTO, CraftDTO


class CraftWriter(Protocol):
    async def create_craft(self, data: CreateCraftDTO) -> CraftDTO:
        raise NotImplementedError
