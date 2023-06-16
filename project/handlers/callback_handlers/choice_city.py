from loader import bot
from telebot.types import CallbackQuery
from loguru import logger

from states.user_states import UserInputState


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
@logger.catch
def city_id_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку города, который ему нужен.
    Записываем id этого города.

    :param call: отклик клавиатуры, получает id города.
    """
    if call.data:
        with bot.retrieve_data(call.message.chat.id) as data:
            data['city_id'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserInputState.amount_hotels)
        bot.send_message(call.message.chat.id, 'Сколько найти отелей?\nНо не более 10!')
