from typing import Protocol

from craftgame.dto.item import CreateItemDTO, ItemDTO


class ItemWriter(Protocol):
    async def create_item(self, data: CreateItemDTO) -> ItemDTO:
        raise NotImplementedError
