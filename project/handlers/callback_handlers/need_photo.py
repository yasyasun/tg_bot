from datetime import date

from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar

from loader import bot
from telebot.types import CallbackQuery
from states.user_states import UserInputState


@bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data == 'no')
@logger.catch
def need_photo_callback(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие кнопки 'да' или 'нет' на вопрос о необходимости загрузить фото отелей.
    Если ответ 'да': записывает состояния пользователя 'photo_need' = True и предлагает ввести количество фото.
    Если ответ 'нет': записывает состояния пользователя 'photo_need' = False и 'photo_amt' = 0 и
    показывает клавиатуру-календарь с выбором даты заезда.

    :param call: отклик клавиатуры 'yes' или 'no'.
    """
    if call.data == 'yes':
        with bot.retrieve_data(call.message.chat.id) as data:
            data['need_photo'] = True
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserInputState.amount_photos)
        bot.send_message(call.message.chat.id, 'Введите количество фото\nОт 1 до 10!')
    elif call.data == 'no':
        with bot.retrieve_data(call.message.chat.id) as data:
            data['need_photo'] = False
            data['amount_photos'] = 0
        bot.delete_message(call.message.chat.id, call.message.message_id)
        calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
        bot.send_message(call.message.chat.id, 'Введите дату заезда', reply_markup=calendar)
    else:
        bot.send_message(call.message.chat.id, text='⚠️ Нажмите кнопку "Да" или "Нет"')
