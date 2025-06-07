from typing import Protocol

from ..dto import CreateUserDTO, UserDTO


class UserWriter(Protocol):
    async def create_user(self, data: CreateUserDTO) -> UserDTO:
        raise NotImplementedError
