from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("types"))
async def cmd_types(message: Message):
    await message.answer(
        text="Отслеживаемые типы:\n"
        "- Аниматор\n"
        "- Аниматор в лаундж\n"
        "- Актер\n"
        "- Актер детский\n"
        "- Фотограф\n"
        "- Треш\n"
        "- Привлечение\n"
        "- Мафия 30 мин\n"
        "- Мафия 60 мин\n"
        "- Диско 30 мин\n"
        "- Диско 60 мин\n"
        "- Мастер теней 30 мин\n"
        "- Мастер теней 60 мин",
    )
