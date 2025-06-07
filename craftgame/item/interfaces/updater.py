from typing import Protocol, Any
from uuid import UUID

from craftgame.user.dto import UpdateUserDTO


class UserUpdater(Protocol):
    async def update_user(self, user_id: UUID, data: UpdateUserDTO) -> None:
        raise NotImplementedError
