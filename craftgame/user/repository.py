from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from craftgame.user.interfaces.repo import UserRepo
from craftgame.user.model import User


@dataclass(frozen=True)
class UserRepository(UserRepo):
    session: AsyncSession

    async def create_user(self, data: dict[str, Any]) -> UUID:
        stmt = insert(User).values(data).returning(User.id)
        result = await self.session.scalar(stmt)
        return result

    async def find_one_user_filtered(self, filters: dict[str, Any]) -> User | None:
        stmt = select(User).where(**filters)
        result = await self.session.scalar(stmt)
        return result

    async def update_user(self, user_id: UUID, data: dict[str, Any]):
        stmt = update(User).values(data).where(User.id == user_id)
        await self.session.execute(stmt)

    async def delete_user(self, user_id: UUID) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
