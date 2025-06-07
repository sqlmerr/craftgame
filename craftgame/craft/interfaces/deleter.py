from typing import Protocol
from uuid import UUID


class CraftDeleter(Protocol):
    async def delete_craft(self, craft_id: UUID) -> None:
        raise NotImplementedError
