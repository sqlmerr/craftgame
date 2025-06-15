from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, delete, select, and_, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.core.interfaces.craft.repo import CraftRepo
from craftgame.models.craft import Craft


@dataclass(frozen=True)
class CraftRepository(CraftRepo):
    session: AsyncSession

    async def create_craft(self, data: dict[str, Any]) -> UUID:
        stmt = insert(Craft).values(data).returning(Craft.id)
        result = await self.session.scalars(stmt)
        return result.one()

    async def find_one_craft_filtered(
        self, filters: ColumnElement[bool]
    ) -> Craft | None:
        stmt = select(Craft).where(filters)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_one_craft_by_ingredients(
        self, ingredient1_id: UUID, ingredient2_id: UUID
    ) -> Craft | None:
        stmt = select(Craft).where(
            and_(
                Craft.ingredient1_id == ingredient1_id,
                Craft.ingredient2_id == ingredient2_id,
            )
            | and_(
                Craft.ingredient2_id == ingredient1_id,
                Craft.ingredient1_id == ingredient1_id,
            )
        )
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def find_all_crafts(self, filters: ColumnElement[bool]) -> list[Craft]:
        stmt = select(Craft).where(filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def delete_craft(self, craft_id: UUID) -> None:
        stmt = delete(Craft).where(Craft.id == craft_id)
        await self.session.execute(stmt)
