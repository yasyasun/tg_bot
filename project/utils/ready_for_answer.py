from typing import Dict

from loguru import logger
from telebot.types import Message

from loader import bot


@logger.catch()
def low_high_price_answer(message: Message, data: Dict, user: str) -> None:
    """
    Функция делает запросы на парсинг отелей и на обработку полученных данных.
    Если данные получены - вызывает функцию show_info.
    Если в результате какого-либо из запросов получает None - показывает сообщение об ошибке.

    :param message: сообщение Telegram
    :param data: словарь с данными запроса (город, даты поездки, нужны ли фото)
    :param user: имя пользователя Telegram (username)
    """

    amount_nights = int((data['end_date'] - data['start_date']).total_seconds() / 86400)
    sort_order = 'дешёвых' if data.get('last_command') == 'lowprice' else 'дорогих'
    reply_str = f"✅ Ок, ищем: <b>топ {data['amount_hotels']}</b> " \
                f"самых {sort_order} отелей в городе <b>{data['city']}</b>\n" \
                f"{f'Нужно загрузить фото' if data['need_photo'] else f'Фото не нужны'}" \
                f" — <b>{data['amount_photo']}</b> штук\n" \
                f"Длительность поездки: <b>{amount_nights} ноч.</b> " \
                f"(с {data['start_date']} по {data['end_date']})."
    bot.send_message(message.chat.id, reply_str, parse_mode="html")

    hotels = parse_hotels(data)
    if hotels:
        result_dict = process_hotels_info(hotels.get('results'), amount_nights)
        if result_dict:
            show_info(message=message, request_data=data, result_data=result_dict, user=user,
                      amount_nights=amount_nights)
        else:
            bot.send_message(message.chat.id, '⚠️ Не удалось загрузить информацию по отелям города!')
    else:
        bot.send_message(message.chat.id, '⚠️ Ошибка. Попробуйте ещё раз!')
