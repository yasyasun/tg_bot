from loguru import logger
from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
@logger.catch
def bot_help(message: Message):
    """
    Функция, реагирующая на команду '/help'. Выводит сообщение со списком команд.

    :param message: сообщение Telegram
    """
    text = [f"<b>/{command}</b> - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, "\n".join(text), parse_mode='html')
