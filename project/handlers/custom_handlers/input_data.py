from loguru import logger
from telebot.types import Message
from datetime import datetime

from keyboards.inline.buttons_for_cities import print_cities
from keyboards.reply.photo import about_photo
from loader import bot
from states.user_states import UserInputState
from utils.get_cities import parse_cities


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@logger.catch
def low_high_best_handler(message: Message) -> None:
    """
    Обработчик команд, срабатывает на три команды /lowprice, /highprice, /bestdeal
    и запоминает необходимые данные. Спрашивает пользователя - какой искать город.

    :param message: сообщение Telegram
    """
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        data['date_time'] = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
    bot.set_state(message.from_user.id, UserInputState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите город поиска\n'
                                           '❗Поиск по городам России на данный момент временно не работает.')


@bot.message_handler(state=UserInputState.city)
@logger.catch
def input_city(message: Message) -> None:
    """
    Ввод пользователем города и отправка запроса серверу на поиск вариантов городов.
    Возможные варианты городов передаются генератору клавиатуры.
    Предлагает ввести количество отелей.

    :param message: сообщение Telegram
    """
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        cities = parse_cities(message.text)
        if cities:
            bot.send_message(message.from_user.id, 'Пожалуйста, уточните:', reply_markup=print_cities(cities))
            bot.delete_message(message.chat.id, message.message_id)
            bot.set_state(message.from_user.id, UserInputState.amount_hotels, message.chat.id)
            bot.send_message(message.from_user.id, 'Сколько найти отелей?\nНо не более 10!')
        else:
            bot.send_message(message.from_user.id, '⚠️ Не нахожу такой город. Введите ещё раз.')
    else:
        bot.send_message(message.from_user.id, '⚠️ Название города может состоять только из букв')


@bot.message_handler(state=UserInputState.amount_hotels)
def input_hotels(message: Message) -> None:
    """
    Ввод количества выдаваемых на странице отелей, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 10

    :param message: сообщение Telegram
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["amt_hotels"] = message.text
            bot.set_state(message.from_user.id, UserInputState.need_photo, message.chat.id)
            bot.send_message(message.from_user.id, "Вам нужны фотографии?", reply_markup=about_photo())
        else:
            bot.send_message(message.chat.id, 'Ошибка! Должно быть число в диапазоне от 1 до 10! Повторите ввод!')
    else:
        bot.send_message(message.from_user.id, "Ошибка! Введите число!")


@bot.message_handler(state=UserInputState.need_photo)
def input_photo(message: Message) -> None:
    """
    Ввод количества фотографий и проверка на число и на соответствие заданному диапазону от 1 до 10.

    :param message: сообщение Telegram
    """
    if message.text == 'Да':
        bot.set_state(message.from_user.id, UserInputState.amount_photos, message.chat.id)
        bot.send_message(message.from_user.id, "Введите количество фотографий")
    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, "Спасибо за запрос!")
    else:
        bot.send_message(message.from_user.id, "Выберите Да или Нет!")
#
#
# @bot.message_handler(state=UserInputState.amt_photos)
# def get_photos(message: Message) -> None:
#     if message.text.isdigit():
#         bot.send_message(message.from_user.id, "Спасибо за запрос!")
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data["amt_photos"] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, "Введите число!")
