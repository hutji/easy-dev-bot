# easy-dev-bot

#  Бот может:
Пользователь может вставлять ссылку на канал с видеохостинга Видеохостинг RUTUBE. Указать кол-во видео для парсинга и получить ответ от бота в виде:
-Наименование видео
-Краткое описание до 100 символов
-Кол-во просмотров
-Ссылка на видео

## Запуск проекта из исходников GitHub

Клонируем себе репозиторий: 

```bash 
git clone git@github.com:hutji/easy-dev-bot.git
```
Создаем файл .env в корневой директории с содержанием файла .env-example:

```
TELEGRAM_TOKEN='your_bot_token'

DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:postgres@localhost:5432/easy-dev
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/easy-dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=easy-dev
DB_HOST=db
DB_PORT=5432
```

Выполняем запуск:

Для запуска бота из корневой директории выполните команду:

```bash
docker compose up
```

# Бот доступен по: 

```
https://t.me/hutji_parser_bot
```

# Основные команды для работы с ботом:

```
/start для запуска бота, бот попросит ввести ссылку на канал и кол-во видео в формате:

https://rutube.ru/channel/23787152/ 5

https://rutube.ru/channel/31195085/ 3
```

```
/view_videos для просмотра раннее сохранненых видео. Пользователь имеет возможность выбрать сохраненный канал и видео канала.
```

## Остановка оркестра контейнеров

В окне, где был запуск **Ctrl+С** или в другом окне:

```bash
docker compose down
```

## Технологии проекта

```Technologies```
* #### aiogram
* #### aiohttp
* #### Python 3.11
* #### alembic
* #### asyncpg
* #### PostgreSQL
* #### Docker
* #### SQLAlchemy
* #### beautifulsoup4
* #### httpx


## Информация об авторе

- Лашков Павел Александрович, backend разработчик, г. Москва
- https://github.com/hutji
