from loguru import logger
from telebot.types import Message
from datetime import datetime, date
from telegram_bot_calendar import DetailedTelegramCalendar

from database.db_handlers import save_user
from keyboards.inline.create_buttons import print_cities, photo_need_yes_or_no
from loader import bot
from states.user_states import UserInputState
from utils.get_cities import parse_cities
from utils.print_data import print_data_from_user


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@logger.catch
def low_high_best_handler(message: Message) -> None:
    """
    Обработчик команд, срабатывает на три команды /lowprice, /highprice, /bestdeal
    и запоминает необходимые данные. Спрашивает пользователя - какой искать город.

    :param message: сообщение Telegram.
    """
    save_user(message)
    bot.delete_state(message.from_user.id, message.chat.id)  # перед началом опроса зачищаем все собранные состояния
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
        data['command'] = message.text
        data['date_time'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        data['user'] = message.from_user.username
    bot.set_state(message.from_user.id, UserInputState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите город поиска\n\n'
                                           '❗Поиск по городам России на данный момент временно не работает.')


@bot.message_handler(state=UserInputState.city)
@logger.catch
def input_city(message: Message) -> None:
    """
    Ввод пользователем города и отправка запроса серверу на поиск вариантов городов.
    Возможные варианты городов передаются генератору клавиатуры.

    :param message: сообщение Telegram.
    """
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        cities = parse_cities(message.text)
        if cities:
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
    введённое числом и входит ли оно в заданный диапазон от 1 до 10.

    :param message: сообщение Telegram.
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
    Ввод количества фотографий, проверка на число и
    на соответствие заданному диапазону от 1 до 10.

    :param message: сообщение Telegram.
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['amount_photos'] = int(message.text)
            calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
            bot.send_message(message.chat.id, 'Введите дату заезда', reply_markup=calendar)
        else:
            bot.send_message(message.from_user.id, '⚠️ Количество фото должно быть от 1 до 10!\n'
                                                   'Пожалуйста, повторите ввод')
    else:
        bot.send_message(message.from_user.id, '⚠️ Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.min_price)
@logger.catch
def input_min_price(message: Message) -> None:
    """
    Функция, ожидающая корректный ввод количества $.
    Записывает состояние пользователя 'min_price' и
    предлагает ввести максимальную цену за ночь.

    :param message: сообщение Telegram.
    """
    if message.text.isdigit():
        if int(message.text) > 0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_price'] = float(message.text)
            bot.set_state(message.from_user.id, UserInputState.max_price, message.chat.id)
            bot.send_message(message.chat.id, "Введите максимальную цену за ночь в $:")
        else:
            bot.send_message(message.from_user.id, '⚠️ Введите число больше нуля')
    else:
        bot.send_message(message.from_user.id, '⚠️ Введите число больше нуля')


@bot.message_handler(state=UserInputState.max_price)
@logger.catch
def input_max_price(message: Message) -> None:
    """
    Функция, ожидающая корректный ввод количества $.
    Записывает состояние пользователя 'max_price' и
    предлагает ввести минимальное расстояние до центра в милях.

    :param message: сообщение Telegram.
    """
    if int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(message.text) > data['min_price']:
                data['max_price'] = float(message.text)
                bot.set_state(message.from_user.id, UserInputState.start_distance, message.chat.id)
                bot.send_message(message.chat.id, "Введите минимальное расстояние до центра в км "
                                                  "(например 5.5):")
            else:
                bot.send_message(message.chat.id,
                                 f"⚠️ Максимальная цена должна быть больше {data['min_price']}$")
    else:
        bot.send_message(message.from_user.id, '⚠️ Введите число больше нуля')


@bot.message_handler(state=UserInputState.start_distance)
@logger.catch
def input_start_distance(message: Message) -> None:
    """
    Функция, ожидающая ввод минимального расстояния до центра.
    Записывает состояние пользователя 'start_distance' и
    предлагает ввести максимальное расстояние до центра в милях.

    :param message: сообщение Telegram.
    """
    if int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['start_distance'] = float(message.text)
            bot.set_state(message.from_user.id, UserInputState.end_distance, message.chat.id)
            bot.send_message(message.chat.id, "Введите максимальное расстояние до центра в км "
                                              "(например 5.5):")
    else:
        bot.send_message(message.from_user.id, '⚠️ Введите число больше нуля')


@bot.message_handler(state=UserInputState.end_distance)
@logger.catch
def input_end_distance(message: Message) -> None:
    """
    Функция, ожидающая ввод максимального расстояния до центра.
    Записывает состояние пользователя 'end_distance', завершает опрос и
    вызывает функцию для подготовки ответа на запрос пользователя.
    Затем ожидает ввода следующей команды.

    :param message: сообщение Telegram.
    """
    if ',' in message.text:
        message.text = message.text.replace(',', '.')
    try:
        message.text = float(message.text)
        if message.text > 0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if message.text > data['start_distance']:
                    data['end_distance'] = message.text
                    data_from_user = data
                    print_data_from_user(message, data_from_user)
                    bot.set_state(message.chat.id, state=None)
                    bot.send_message(message.chat.id, f"😉👌 Можете ввести другую команду!\n"
                                                      f"Например: <b>/help</b>", parse_mode="html")
                else:
                    bot.send_message(
                        message.chat.id,
                        f"⚠️ Максимальное расстояние от центра должна быть больше {data['start_distance']}$"
                    )
        else:
            bot.send_message(message.from_user.id, '⚠️ Введите число больше нуля')
    except Exception:
        bot.set_state(message.chat.id, state=None)
        bot.send_message(message.chat.id, "⚠️ Ошибка. Попробуйте еще раз.\n")
