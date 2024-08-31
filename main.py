import asyncio
import importlib
import pkgutil

from aiogram import Bot, Dispatcher

from src import handlers
from src.config import settings
from src.middlewares.owner_check import OnlyOwnerMiddleware


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    for x in pkgutil.iter_modules(handlers.__path__):
        handler = importlib.import_module("src.handlers." + x.name)
        router = handler.router
        router.message.middleware(OnlyOwnerMiddleware())
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
