from loguru import logger
from telebot.types import Message

from database.db_handlers import save_user
from loader import bot


@bot.message_handler(commands=["start"])
@logger.catch
def bot_start(message: Message):
    """
    Функция, реагирующая на команду '/start'. Выводит приветственное сообщение.

    :param message: сообщение Telegram
    """
    save_user(message)
    bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.full_name}!\n"
                                           f"Можете ввести какую-нибудь команду!\n"
                                           f"Например: <b>/help</b>", parse_mode='html')
