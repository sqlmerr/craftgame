from typing import Protocol
from ..dto import GenerateItemDTO, GeneratedItemDTO


class ItemGenerator(Protocol):
    async def generate_item(self, data: GenerateItemDTO) -> GeneratedItemDTO | None:
        raise NotImplementedError
