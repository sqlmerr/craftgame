from typing import Protocol, Any
from uuid import UUID

from sqlalchemy import ColumnElement

from craftgame.models.user import User


class UserRepo(Protocol):
    async def create_user(self, data: dict[str, Any]) -> UUID:
        raise NotImplementedError

    async def find_one_user_filtered(self, filters: ColumnElement[bool]) -> User | None:
        raise NotImplementedError

    async def update_user(self, user_id: UUID, data: dict[str, Any]):
        raise NotImplementedError

    async def delete_user(self, user_id: UUID) -> None:
        raise NotImplementedError
