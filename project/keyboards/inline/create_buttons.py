from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, List
from loguru import logger

from database.models import History
from utils.factories import for_history


@logger.catch
def print_cities(cities_dict: Dict[int, str]) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - выбор подходящего по названию города, из которых пользователь выбирает нужный ему.

    :param cities_dict: словарь с названиями городов и их id.
    :return: клавиатура InlineKeyboardMarkup.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)

    for city_id, city in cities_dict.items():
        keyboard.add(InlineKeyboardButton(text=city, callback_data=city_id))
    return keyboard


@logger.catch
def photo_need_yes_or_no() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками 'Да' и 'Нет'.

    :return: клавиатура InlineKeyboardMarkup
    """
    keyboard_yes_no = InlineKeyboardMarkup(row_width=2)
    keyboard_yes_no.add(
        InlineKeyboardButton(text='ДА', callback_data='yes'),
        InlineKeyboardButton(text='НЕТ', callback_data='no')
    )
    return keyboard_yes_no


@logger.catch
def get_history_action() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - выбор действия с историей поиска.

    :return: клавиатура InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Показать историю поиска', callback_data='show_history'),
        InlineKeyboardButton(text='Очистить историю', callback_data='delete_history')
    )
    return keyboard


@logger.catch
def print_histories(histories_list: List[History]) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками с историей поиска.
    Каждая кнопка: "дата запроса — название команды — город поиска".

    :param histories_list: список с историями поиска пользователя. Каждая история - объект класса History.
    :return: клавиатура InlineKeyboardMarkup.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    for history in histories_list:
        text = f'{history.date} — {history.command} — {history.city}'
        keyboard.add(InlineKeyboardButton(text=text, callback_data=for_history.new(history_id=history.id)))
    return keyboard
