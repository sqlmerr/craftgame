from typing import Protocol

from ..dto import CreateItemDTO, ItemDTO


class ItemWriter(Protocol):
    async def create_item(self, data: CreateItemDTO) -> ItemDTO:
        raise NotImplementedError
