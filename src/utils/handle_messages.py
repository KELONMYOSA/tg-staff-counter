import re

from aiogram.types import Message

from src.db.crud import Database


def handle_msg(message: Message):
    if not message.text or "@Qguru_kzn_bot" not in message.text:
        return

    patterns = {
        "Аниматор": r"[Аа]ниматор\s*[:\s]?\s*(\d+)",
        "Аниматор в лаундж": r"[Аа]ниматор в лаундж\s*[:\s]?\s*(\d+)",
        "Актер": r"[Аа]ктер\s*[:\s]?\s*(\d+)",
        "Актер детский": r"[Аа]ктер детский\s*[:\s]?\s*(\d+)",
        "Фотограф": r"[Фф]отограф\s*[:\s]?\s*(\d+)",
        "Треш": r"[Тт]реш\s*[:\s]?\s*(\d+)",
        "Мафия 30 мин": r"[Мм]афия 30 мин\s*[:\s]?\s*(\d+)",
        "Мафия 60 мин": r"[Мм]афия 60 мин\s*[:\s]?\s*(\d+)",
        "Диско 30 мин": r"[Дд]иско 30 мин\s*[:\s]?\s*(\d+)",
        "Диско 60 мин": r"[Дд]иско 60 мин\s*[:\s]?\s*(\d+)",
        "Привлечение": r"[Пп]ривлечение\s*[:\s]?\s*(\d+)",
        "Мастер теней 30 мин": r"[Мм]астер теней 30 мин\s*[:\s]?\s*(\d+)",
        "Мастер теней 60 мин": r"[Мм]астер теней 60 мин\s*[:\s]?\s*(\д+)",
    }

    timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")
    tg_id = message.from_user.id
    tg_username = message.from_user.username
    link = f"https://t.me/c/{str(message.chat.id)[-10:]}/{message.message_id}"

    for msg_type, pattern in patterns.items():
        match = re.search(pattern, message.text)
        if match:
            count = int(match.group(1))
            with Database() as db:
                db.add_msg(msg_type, timestamp, tg_id, tg_username, count, link)


def get_report(start_date: str, end_date: str) -> str:
    with Database() as db:
        records = db.get_between_dates(start_date, end_date)

    if records:
        category_stats = {}
        type_totals = {}

        for record in records:
            msg_type = record[0]
            username = record[3]
            count = record[4]

            if msg_type not in category_stats:
                category_stats[msg_type] = {}
            if username not in category_stats[msg_type]:
                category_stats[msg_type][username] = 0

            category_stats[msg_type][username] += count

            if msg_type not in type_totals:
                type_totals[msg_type] = 0
            type_totals[msg_type] += count

        report = ""
        for msg_type, users in category_stats.items():
            report += f"{msg_type}:\n"
            for username, count in users.items():
                report += f"@{username} - {count}\n"
            report += "\n"

        report += "Итого за период:\n"
        for msg_type, total in type_totals.items():
            report += f"{msg_type}: {total}\n"

        return f"<b>Отчет с {start_date} по {end_date}:</b>\n\n{report}"
    else:
        return f"Записи за период с {start_date} по {end_date} не найдены."
