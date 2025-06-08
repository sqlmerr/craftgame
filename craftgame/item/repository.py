from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update, delete, select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.item.interfaces.repo import ItemRepo
from craftgame.item.model import Item


@dataclass(frozen=True)
class ItemRepository(ItemRepo):
    session: AsyncSession

    async def create_item(self, data: dict[str, Any]) -> UUID:
        stmt = insert(Item).values(data).returning(Item.id)
        result = await self.session.scalars(stmt)
        return result.one()

    async def find_one_item_filtered(self, filters: ColumnElement[bool]) -> Item | None:
        stmt = select(Item).where(filters)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_all_items(self, filters: ColumnElement[bool]) -> list[Item]:
        stmt = select(Item).where(filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def update_item(self, item_id: UUID, data: dict[str, Any]):
        stmt = update(Item).values(data).where(Item.id == item_id)
        await self.session.execute(stmt)

    async def delete_item(self, item_id: UUID) -> None:
        stmt = delete(Item).where(Item.id == item_id)
        await self.session.execute(stmt)
