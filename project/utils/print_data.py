from typing import Dict

from loguru import logger
from telebot.types import Message

from loader import bot
from utils.get_hotels import parse_and_print_hotels


@logger.catch()
def print_data_from_user(message: Message, data: Dict) -> None:
    """
    Выводим в чат всё, что собрали от пользователя и передаем это
    в функцию поиска отелей.

    :param message: сообщение Telegram.
    :param data: словарь со всеми данными запроса.
    """

    amount_nights = int((data['end_date'] - data['start_date']).total_seconds() / 86400)
    sort_order = 'дешёвых' if data.get('command') == '/lowprice' else 'дорогих'
    if data['command'] == '/bestdeal':
        reply_str = f"✅ Ок, ищем:\n" \
                    f"<b>Топ {data['amount_hotels']}</b> отеля(ей) в городе <b>{data['city']}</b>\n" \
                    f"В ценовом диапазоне <b>от {data['min_price']} до {data['max_price']}$</b>\n" \
                    f"Максимальная удаленность от центра: " \
                    f"<b>от {data['start_distance']} до {data['end_distance']} км</b>\n" \
                    f"Фото: <b>{data['amount_photos']}</b> шт.\n" \
                    f"Длительность поездки: <b>{amount_nights}</b> ноч.\n" \
                    f"с <b>{data['start_day']}-{data['start_month']}-{data['start_year']}</b> " \
                    f"по <b>{data['end_day']}-{data['end_month']}-{data['end_year']}</b>"
    else:
        reply_str = f"✅ Ок, ищем:\n" \
                    f"<b>Топ {data['amount_hotels']}</b> из самых {sort_order} отелей\n" \
                    f"в городе <b>{data['city']}</b>\n" \
                    f"Фото: <b>{data['amount_photos']}</b> шт.\n" \
                    f"Длительность поездки: <b>{amount_nights}</b> ноч.\n" \
                    f"с <b>{data['start_day']}-{data['start_month']}-{data['start_year']}</b> " \
                    f"по <b>{data['end_day']}-{data['end_month']}-{data['end_year']}</b>"

    bot.send_message(message.chat.id, reply_str, parse_mode="html")
    parse_and_print_hotels(message, data)
