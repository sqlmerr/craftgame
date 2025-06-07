from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update, delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.craft.interfaces.repo import CraftRepo
from craftgame.craft.model import Craft


@dataclass(frozen=True)
class CraftRepository(CraftRepo):
    session: AsyncSession
    

    async def create_craft(self, data: dict[str, Any]) -> UUID:
        stmt = insert(Craft).values(data).returning(Craft.id)
        result = await self.session.scalars(stmt)
        return result.one()

    async def find_one_craft_filtered(self, filters: dict[str, Any]) -> Craft | None:
        stmt = select(Craft).where(**filters)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_one_craft_by_ingredients(self, ingredient1_id: UUID, ingredient2_id: UUID) -> Craft | None:
        stmt = select(Craft).where(
            and_(Craft.ingredient1_id == ingredient1_id, Craft.ingredient2_id == ingredient2_id) | and_(
                Craft.ingredient2_id == ingredient1_id, Craft.ingredient1_id == ingredient1_id
            )
        )
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_all_crafts(self, filters: dict[str, Any]) -> list[Craft]:
        stmt = select(Craft).where(**filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def delete_craft(self, craft_id: UUID) -> None:
        stmt = delete(Craft).where(Craft.id == craft_id)
        await self.session.execute(stmt)
