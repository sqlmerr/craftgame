from typing import Protocol
from uuid import UUID

from craftgame.dto.user import UpdateUserDTO


class UserUpdater(Protocol):
    async def update_user(self, user_id: UUID, data: UpdateUserDTO) -> None:
        raise NotImplementedError
