# Телеграм бот для учета времени

## Как запустить:

### 1. Клонировать репозиторий

```bash
git clone https://github.com/KELONMYOSA/tg-staff-counter.git
```

### 2. Создать .env файл

#### .env example

```
BOT_TOKEN=TgB0tT0k3N
OWNER_USERNAME=owner_user
```

### 3. Создать SQLite базу данных из SQL файла

```bash
sqlite3 src/db/database.sqlite < src/db/init_db.sql
```

### 4. Запустить docker-compose

```bash
docker compose up -d
```