from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.inventory.interfaces.repo import InventoryRepo
from craftgame.inventory.model import Inventory


@dataclass(frozen=True)
class InventoryRepository(InventoryRepo):
    session: AsyncSession

    async def create_inventory(self, data: dict[str, Any]) -> UUID:
        stmt = insert(Inventory).values(data).returning(Inventory.id)
        result = await self.session.scalars(stmt)
        return result.one()

    async def find_one_inventory_filtered(
        self, filters: dict[str, Any]
    ) -> Inventory | None:
        stmt = select(Inventory).where(**filters)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_all_inventories(self, filters: dict[str, Any]) -> list[Inventory]:
        stmt = select(Inventory).where(**filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def update_inventory(self, inventory_id: UUID, data: dict[str, Any]):
        stmt = update(Inventory).values(data).where(Inventory.id == inventory_id)
        await self.session.execute(stmt)

    async def delete_inventory(self, inventory_id: UUID) -> None:
        stmt = delete(Inventory).where(Inventory.id == inventory_id)
        await self.session.execute(stmt)
