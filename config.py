import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

bot_token = os.getenv("TELEGRAM_TOKEN")
database_url_async = os.getenv("DATABASE_URL_ASYNC")
database_url = os.getenv("DATABASE_URL")
