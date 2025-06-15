from typing import Protocol
from uuid import UUID


class UserDeleter(Protocol):
    async def delete_user(self, user_id: UUID) -> None:
        raise NotImplementedError
