CREATE TABLE IF NOT EXISTS animator_messages
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    tg_id INTEGER NOT NULL,
    tg_username TEXT,
    count INTEGER NOT NULL,
    link TEXT NOT NULL
);