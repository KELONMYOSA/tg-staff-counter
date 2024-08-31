from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.config import settings


class OnlyOwnerMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        if event.from_user.username != settings.OWNER_USERNAME and (event.text and event.text.startswith("/")):
            await event.answer("Доступ к функционалу есть только у администратора!")
            return
        return await handler(event, data)
