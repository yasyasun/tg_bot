from telebot.types import Message

from keyboards.inline.create_buttons import get_history_action
from loader import bot
from loguru import logger

from states.user_states import UserInputState


@bot.message_handler(commands=['history'])
@logger.catch
def history_command(message: Message):
    """
    Функция, реагирующая на команду 'history'.
    Показывает клавиатуру с выбором действия: 'Показать историю поиска' или 'Очистить историю'.

    :param message: сообщение Telegram.
    """
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user'] = message.from_user.username
    bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=get_history_action())
