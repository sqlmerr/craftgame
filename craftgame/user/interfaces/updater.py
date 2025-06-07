from typing import Protocol, Any


class UserUpdater(Protocol):
    async def update_user(self, data: dict[str, Any]) -> None:
        raise NotImplementedError
