import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("5811515186:AAFNv4N4FxG3PKBEd0PoOkpN0sMLOExtDSU")
RAPID_API_KEY = os.getenv("537090d3f5msh85dc7d5dad03ed7p13abffjsn13a4aa3a0315")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
("lowprice","Вывести список недорогих отелей"),
("highprice","Вывести список дорогих отелей"),
("bestdeal","Вывести список отелей по фильтрам"),
("history","Вывести историю поиска"))