from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import Dict
from loguru import logger

from loader import bot


@logger.catch
def print_cities(cities_dict: Dict[str, str]) -> InlineKeyboardMarkup:
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
