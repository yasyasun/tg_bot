from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict
from loguru import logger


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
