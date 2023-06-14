from typing import Dict
from loguru import logger
from telebot.types import Message
from datetime import datetime, date
from telegram_bot_calendar import DetailedTelegramCalendar

from keyboards.inline.create_buttons import print_cities, photo_need_yes_or_no
from loader import bot
from states.user_states import UserInputState
from utils.get_cities import parse_cities


LSTEP_RU: Dict[str, str] = {'y': 'год', 'm': 'месяц', 'd': 'день'}


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@logger.catch
def low_high_best_handler(message: Message) -> None:
    """
    Обработчик команд, срабатывает на три команды /lowprice, /highprice, /bestdeal
    и запоминает необходимые данные. Спрашивает пользователя - какой искать город.

    :param message: сообщение Telegram
    """
    bot.delete_state(message.from_user.id, message.chat.id)  # перед началом опроса зачищаем все собранные состояния
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        data['date_time'] = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
    print(data)
    bot.set_state(message.from_user.id, UserInputState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите город поиска\n\n'
                                           '❗Поиск по городам России на данный момент временно не работает.')


@bot.message_handler(state=UserInputState.city)
@logger.catch
def input_city(message: Message) -> None:
    """
    Ввод пользователем города и отправка запроса серверу на поиск вариантов городов.
    Возможные варианты городов передаются генератору клавиатуры.

    :param message: сообщение Telegram
    """
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        cities = parse_cities(message.text)
        if cities:
            bot.set_state(message.from_user.id, UserInputState.amount_hotels, message.chat.id)
            bot.send_message(message.from_user.id, 'Пожалуйста, уточните:', reply_markup=print_cities(cities))
        else:
            bot.send_message(message.from_user.id, '⚠️ Не нахожу такой город. Введите ещё раз.')
    else:
        bot.send_message(message.from_user.id, '⚠️ Название города может состоять только из букв')


@bot.message_handler(state=UserInputState.amount_hotels)
@logger.catch
def input_hotels(message: Message) -> None:
    """
    Ввод количества выдаваемых отелей, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 10

    :param message: сообщение Telegram
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['amount_hotels'] = int(message.text)
            bot.send_message(message.from_user.id,
                             'Желаете загрузить фото отелей?',
                             reply_markup=photo_need_yes_or_no())
        else:
            bot.send_message(message.from_user.id, '⚠️ Количество отелей должно быть от 1 до 10!\n'
                                                   'Пожалуйста, повторите ввод.')
    else:
        bot.send_message(message.from_user.id, '⚠️ Ошибка!\nВведите число!')


@bot.message_handler(state=UserInputState.amount_photos)
@logger.catch
def input_photo(message: Message) -> None:
    """
    Ввод количества фотографий, проверка на число и на соответствие заданному диапазону от 1 до 10.

    :param message: сообщение Telegram
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['amount_photos'] = int(message.text)
            calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
            bot.send_message(message.chat.id, f"Введите дату заезда", reply_markup=calendar)
        else:
            bot.send_message(message.from_user.id, '⚠️ Количество фото должно быть от 1 до 10!\n'
                                                   'Пожалуйста, повторите ввод')
    else:
        bot.send_message(message.from_user.id, '⚠️ Ошибка! Вы ввели не число! Повторите ввод!')



