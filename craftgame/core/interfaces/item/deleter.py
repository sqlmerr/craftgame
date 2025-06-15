from typing import Protocol
from uuid import UUID


class ItemDeleter(Protocol):
    async def delete_item(self, item_id: UUID) -> None:
        raise NotImplementedError
