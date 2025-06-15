from typing import Protocol

from craftgame.dto.user import CreateUserDTO, UserDTO


class UserWriter(Protocol):
    async def create_user(self, data: CreateUserDTO) -> UserDTO:
        raise NotImplementedError
