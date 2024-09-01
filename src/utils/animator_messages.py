import re

import pandas as pd
from aiogram.types import Message

from src.db.crud import Database


def handle_animator_msg(message: Message):
    pattern = r"Аниматор:\s*(\d+)"
    match = re.search(pattern, message.text)

    if match:
        timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")
        tg_id = message.from_user.id
        tg_username = message.from_user.username
        count = int(match.group(1))
        link = f"https://t.me/c/{str(message.chat.id)[-10:]}/{message.message_id}"
        with Database() as db:
            db.add_animator_msg(timestamp, tg_id, tg_username, count, link)


def get_animator_report(start_date: str, end_date: str) -> str:
    with Database() as db:
        records = db.get_animator_between_dates(start_date, end_date)
    if records:
        user_stats = {}
        for record in records:
            username = record[2]
            count = record[3]
            if username in user_stats:
                user_stats[username] += count
            else:
                user_stats[username] = count
        report = ""
        total = 0
        for username in user_stats:
            total += user_stats[username]
            report += f"@{username}\nАниматор: {user_stats[username]}\n\n"
        report += f"Итого за период\nАниматор: {total}\n\n"

        df = pd.DataFrame(records, columns=["Дата и время", "TG ID", "TG Username", "Количество", "Ссылка"])
        logs = df.to_string(index=False)
        return f"<b>Отчет с {start_date} по {end_date}:</b>\n\n{report}<pre>{logs}</pre>"
    else:
        return f"Записи за период с {start_date} по {end_date} не найдены."
