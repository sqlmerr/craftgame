from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update, delete, select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.core.interfaces.inventory.repo import InventoryRepo
from craftgame.models.inventory import InventoryItem


@dataclass(frozen=True)
class InventoryRepository(InventoryRepo):
    session: AsyncSession

    async def create_inventory_item(self, data: dict[str, Any]) -> UUID:
        stmt = insert(InventoryItem).values(data).returning(InventoryItem.id)
        result = await self.session.scalars(stmt)
        return result.one()

    async def find_one_inventory_item_filtered(
        self, filters: ColumnElement[bool]
    ) -> InventoryItem | None:
        stmt = select(InventoryItem).where(filters)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_all_inventory_items(
        self, filters: ColumnElement[bool]
    ) -> list[InventoryItem]:
        stmt = select(InventoryItem).where(filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def update_inventory_item(self, inventory_id: UUID, data: dict[str, Any]):
        stmt = (
            update(InventoryItem).values(data).where(InventoryItem.id == inventory_id)
        )
        await self.session.execute(stmt)

    async def delete_inventory_item(self, inventory_id: UUID) -> None:
        stmt = delete(InventoryItem).where(InventoryItem.id == inventory_id)
        await self.session.execute(stmt)
