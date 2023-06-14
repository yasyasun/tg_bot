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

    :param call: отклик клавиатуры, получает id города
    """
    if call.data:
        bot.set_state(call.from_user.id, UserInputState.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['city_id'] = call.data
