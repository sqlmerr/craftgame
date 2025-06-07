from typing import Protocol, Any
from uuid import UUID

from craftgame.item.model import Item


class ItemRepo(Protocol):
    async def create_item(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_item_filtered(self, filters: dict[str, Any]) -> Item | None:
        raise NotImplementedError

    async def find_all_items(self, filters: dict[str, Any]) -> list[Item]:
        raise NotImplementedError

    async def update_item(self, item_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_item(self, item_id: UUID) -> None:
        raise NotImplementedError
