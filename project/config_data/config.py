import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("lowprice", "Топ самых дешёвых отелей в городе"),
    ('highprice', "Топ самых дорогих отелей в городе"),
    ('bestdeal', "Топ отелей, наиболее подходящих по цене и расположению от центра"),
    ('history', "История поиска отелей"),
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'database' / 'search_history.db'
LOG_PATH = BASE_DIR / 'logs' / 'debug.log'
