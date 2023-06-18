import re

from loguru import logger
from telebot.types import CallbackQuery, InputMediaPhoto

from database.db_handlers import show_history, delete_history
from database.models import db, SearchResult
from loader import bot
from utils.factories import for_history
from utils.get_hotels import print_hotel_info


@bot.callback_query_handler(func=lambda call: call.data == 'show_history' or call.data == 'delete_history')
@logger.catch
def process_history_reply(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие кнопки с выбором действия.
    В зависимости он нажатой кнопки вызывает нужную функцию:
    'Показать историю поиска' или 'Очистить историю'.

    :param call: отклик клавиатуры.
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "show_history":
        try:
            show_history(call.message, user=call.from_user.username)
        except Exception:
            bot.send_message(call.message.chat.id, text='⚠️Упс... ошибка: не могу загрузить историю поиска:')
    elif call.data == "delete_history":
        try:
            delete_history(call.message, user=call.from_user.username)
        except Exception:
            bot.send_message(call.message.chat.id, text='⚠️Упс... ошибка: не могу удалить историю поиска:')


@bot.callback_query_handler(func=None, history_config=for_history.filter())
@logger.catch
def clarify_history(call: CallbackQuery) -> None:
    """
    Функция ловит нажатие кнопки с выбором старых запросов, формирует результат из БД в список.
    Затем присваивает этот список пейджеру 'my_pages'
    и вызывает пагинатор 'show_paginator', который и отобразит результат.

    :param call: отклик клавиатуры.
    """

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    history_date = int(re.search(r'\d+', call.data).group())
    with db:
        results = [result for result in SearchResult.select().where(SearchResult.from_date == history_date)]
        for result in results:
            hotel_data = {
                'name': result.hotel_name,
                'distance_city_center': result.distance_city_center,
                'price_per_night': result.price_per_night,
                'total_price': result.total_price,
                'hotel_address': result.hotel_address
            }
            hotel_info = print_hotel_info(hotel_data=hotel_data, amount_nights=result.amount_nights)
            if hotel_data['need_photo']:
                images = [
                    InputMediaPhoto(media=url, caption=hotel_info) if index == 0 else InputMediaPhoto(media=url)
                    for index, url in enumerate(result.images)
                ]
                bot.send_media_group(call.message.chat.id, images)
            else:
                bot.send_message(call.message.chat.id, hotel_info)
