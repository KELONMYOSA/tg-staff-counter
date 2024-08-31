from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

router = Router()

cmd_list = ["/start"]


@router.message(~F.text.in_(cmd_list))
async def echo_all(message: Message):
    if message.text and message.text.startswith("/"):
        try:
            await message.delete()
        except TelegramBadRequest as e:
            print(e)
        await message.answer(text=f'Я не знаю такую команду: "{message.text}"')
    else:
        print(
            f"Сообщение из группы {message.chat.title} ({message.chat.id}):"
            f" {message.from_user.username}: {message.text}"
        )
