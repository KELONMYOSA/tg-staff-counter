CREATE TABLE IF NOT EXISTS messages
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    tg_id INTEGER NOT NULL,
    tg_username TEXT,
    count INTEGER NOT NULL,
    link TEXT NOT NULL
);