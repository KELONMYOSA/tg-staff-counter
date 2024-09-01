from datetime import timedelta

import pandas as pd
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.db.crud import Database

router = Router()


@router.message(Command("logs"))
async def cmd_logs(message: Message):
    now = message.date
    start_date = (now - timedelta(days=45)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = now.strftime("%Y-%m-%d %H:%M:%S")

    with Database() as db:
        records = db.get_between_dates(start_date, end_date)
    if records:
        df = pd.DataFrame(records, columns=["Тип", "Дата и время", "TG ID", "TG Username", "Количество", "Ссылка"])
        logs = df.to_string(index=False)
        await message.answer(f"<b>Логи с {start_date} по {end_date}:</b>\n\n<pre>{logs}</pre>", parse_mode="HTML")
    else:
        await message.answer(f"Логи за период с {start_date} по {end_date} не найдены.")
