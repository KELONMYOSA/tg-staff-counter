import sqlite3


class Database:
    __DB_PATH = "src/db/database.sqlite"

    # Устанавливаем соединение с базой данных
    def __init__(self, db_location: str | None = None):
        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.__DB_PATH)
        self.cur = self.connection.cursor()

    def __enter__(self):
        return self

    # Сохраняем изменения и закрываем соединение
    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    # Сохраняем сообщение с информацией об аниматорах
    def add_animator_msg(self, timestamp: str, tg_id: int, tg_username: str | None, count: int, link: str):
        self.cur.execute(
            "INSERT INTO animator_messages (timestamp, tg_id, tg_username, count, link) VALUES (?, ?, ?, ?, ?)",
            (timestamp, tg_id, tg_username, count, link),
        )

    # Получаем сообщения с информацией об аниматорах в диапазоне дат
    def get_animator_between_dates(self, start_date: str, end_date: str):
        self.cur.execute(
            "SELECT timestamp, tg_id, tg_username, count, link FROM animator_messages WHERE timestamp BETWEEN ? AND ?",
            (start_date, end_date),
        )
        return self.cur.fetchall()
