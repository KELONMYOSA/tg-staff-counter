from datetime import timedelta

import pandas as pd
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from src.db.crud import Database

router = Router()


@router.message(Command("logs"))
async def cmd_logs(message: Message):
    now = message.date + +timedelta(hours=3)
    start_date = (now - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = now.strftime("%Y-%m-%d %H:%M:%S")

    with Database() as db:
        records = db.get_between_dates(start_date, end_date)

    if records:
        df = pd.DataFrame(records, columns=["Тип", "Дата и время", "TG ID", "TG Username", "Количество", "Ссылка"])

        file_path = "logs.csv"
        df.to_csv(file_path, index=False)

        log_file = FSInputFile(file_path)
        await message.answer_document(document=log_file, caption=f"Логи с {start_date} по {end_date}")
    else:
        await message.answer(f"Логи за период с {start_date} по {end_date} не найдены.")
