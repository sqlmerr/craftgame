from typing import Protocol

from ..dto import CreateCraftDTO, CraftDTO


class CraftWriter(Protocol):
    async def create_craft(self, data: CreateCraftDTO) -> CraftDTO:
        raise NotImplementedError
