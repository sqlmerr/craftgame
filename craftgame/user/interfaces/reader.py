from typing import Protocol
from uuid import UUID

from ..dto import UserDTO


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        raise NotImplementedError

    async def get_user_by_tg_id(self, tg_id: int) -> UserDTO | None:
        raise NotImplementedError
