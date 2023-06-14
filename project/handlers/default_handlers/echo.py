from loguru import logger
from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
@logger.catch
def bot_echo(message: Message):
    """
    Эхо хендлер, куда летят текстовые сообщения без указанного состояния.
    Также функция реагирует на ввод пользователем сообщения 'привет'.

    :param message: сообщение Telegram
    """
    if message.text.lower() == 'привет':
        bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                              f"Введи команду /help для вывода справки")
    else:
        bot.reply_to(message, "Нет такой команды.\n"
                              "Нажмите /help для вывода справки")
