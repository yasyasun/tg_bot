from datetime import timedelta, date
from typing import Dict

from loguru import logger
from telebot.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar

from loader import bot
from states.user_states import UserInputState
from utils.print_data import print_data_from_user

LSTEP_RU: Dict[str, str] = {'y': 'год', 'm': 'месяц', 'd': 'день'}


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
@logger.catch
def date_reply(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие кнопки на клавиатуре-календаре.
    Проверяет, записаны ли состояния 'start_date' и 'end_date'.
    Если нет - снова предлагает выбрать дату и записывает эти состояния.
    Если да, то проверяет состояние пользователя 'last_command'.
    Если 'command' == '/lowprice' или '/highprice' - завершает опрос и
    вызывает функцию для подготовки ответа на запрос пользователя. Затем ожидает ввода следующей команды.
    Иначе продолжает опрос и предлагает ввести минимальную цену за ночь.

    :param call: отклик клавиатуры.
    """

    with bot.retrieve_data(call.message.chat.id) as data:
        if not data.get('start_date'):
            result, key, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru').process(call.data)
        elif not data.get('end_date'):
            new_start_date = data.get('start_date') + timedelta(1)
            result, key, step = DetailedTelegramCalendar(min_date=new_start_date, locale='ru').process(call.data)

    if not result and key:
        bot.edit_message_text(f'Выберите {LSTEP_RU[step]}',
                              call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        with bot.retrieve_data(call.message.chat.id) as data:
            if not data.get('start_date'):
                data['start_date'] = result
                data['start_year'], data['start_month'], data['start_day'] = str(result).split('-')
                calendar, step = DetailedTelegramCalendar(min_date=result + timedelta(1)).build()
                bot.edit_message_text('Введите дату выезда',
                                      call.message.chat.id, call.message.message_id, reply_markup=calendar)
            elif not data.get('end_date'):
                data['end_date'] = result
                data['end_year'], data['end_month'], data['end_day'] = str(result).split('-')

                bot.delete_message(call.message.chat.id, call.message.message_id)

                if data.get('command') in ('/lowprice', '/highprice'):
                    data_from_user = data
                    print_data_from_user(call.message, data_from_user)
                    bot.set_state(call.message.chat.id, state=None)
                    bot.send_message(call.message.chat.id,
                                     f"😉👌 Можете ввести другую команду!\n"
                                     f"Например: <b>/help</b>", parse_mode="html")
                else:
                    bot.set_state(call.from_user.id, UserInputState.min_price, call.message.chat.id)
                    bot.send_message(call.message.chat.id, "Введите минимальную цену за ночь в $:")
