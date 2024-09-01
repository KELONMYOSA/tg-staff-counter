from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message

from src.utils.handle_messages import handle_msg

router = Router()

cmd_list = ["/start", "/get_report", "/types", "/logs"]


@router.message(~F.text.in_(cmd_list), StateFilter(None))
async def echo_all(message: Message):
    if message.text and message.text.startswith("/"):
        try:
            await message.delete()
        except TelegramBadRequest as e:
            print(e)
        await message.answer(text=f'Я не знаю такую команду: "{message.text}"')
    else:
        handle_msg(message)
