from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from dishka import AsyncContainer

from craftgame.common.exceptions import AppError
from craftgame.user.dto import CreateUserDTO
from craftgame.user.service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        container: AsyncContainer = data["dishka_container"]
        from_user: User = data["event_from_user"]

        async with container() as c:
            user_service = await c.get(UserService)
        user = await user_service.get_user_by_tg_id(from_user.id)
        if not user:
            try:
                user = await user_service.create_user(CreateUserDTO(from_user.id))
            except AppError:
                return None
        data["user"] = user

        return await handler(event, data)
