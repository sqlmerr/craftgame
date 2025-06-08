from dataclasses import dataclass
from typing import Any
from uuid import UUID

from craftgame.common.exceptions import ServerError
from craftgame.user.dto import UserDTO, CreateUserDTO, UpdateUserDTO
from craftgame.user.exceptions import UserWithThisTelegramIdAlreadyExists
from craftgame.user.interfaces import UserReader, UserWriter, UserDeleter, UserUpdater
from craftgame.user.interfaces.repo import UserRepo
from craftgame.user.model import User


@dataclass(frozen=True)
class UserService(UserReader, UserWriter, UserDeleter, UserUpdater):
    repository: UserRepo

    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        user = await self.repository.find_one_user_filtered(User.id == user_id)
        if user:
            return UserDTO(
                id=user.id,
                tg_id=user.tg_id,
            )
        return None

    async def get_user_by_tg_id(self, tg_id: int) -> UserDTO | None:
        user = await self.repository.find_one_user_filtered(User.tg_id == tg_id)
        if user:
            return UserDTO(
                id=user.id,
                tg_id=user.tg_id,
            )
        return None

    async def create_user(self, data: CreateUserDTO) -> UserDTO:
        usr = await self.get_user_by_tg_id(data.tg_id)
        if usr is not None:
            raise UserWithThisTelegramIdAlreadyExists

        user_id = await self.repository.create_user({"tg_id": data.tg_id})
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ServerError
        return user

    async def delete_user(self, user_id: UUID) -> None:
        await self.repository.delete_user(user_id)

    async def update_user(self, user_id: UUID, data: UpdateUserDTO) -> None:
        await self.repository.update_user(user_id, data.__dict__)
