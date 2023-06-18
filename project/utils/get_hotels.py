import json
import random
from typing import Dict

from loguru import logger
from telebot.types import Message, InputMediaPhoto

from database.db_handlers import save_results
from loader import bot
from utils.api_request import api_request


@logger.catch
def print_hotel_info(hotel_data: Dict, amount_nights: int) -> str:
    """
    Функция преобразует данные по отелю из словаря в строку.
    Используется для вывода информации.

    :param hotel_data: словарь с информацией по отелю.
    :param amount_nights: количество ночей.
    :return: строка с информацией по отелю.
    """

    result = f"🏩 Отель: {hotel_data['name']}\n" \
             f"🚕 Расстояние до центра: {round(hotel_data['distance'] * 1.61, 1)} км\n" \
             f"💲 Цена за 1 ночь: от {int(hotel_data['price'])}$\n" \
             f"💵 Примерная стоимость за {amount_nights} ноч.: {int(hotel_data['price'] * amount_nights)}$\n" \
             f"⚓️ Адрес отеля: {hotel_data['address']}"
    return result


@logger.catch
def parse_and_print_hotels(message: Message, data_from_user: Dict) -> None:
    """
    Формирование запросов на поиск отелей и детальной информации о них (адрес, фотографии).
    Вывод полученных данных пользователю в чат.

    :param message: сообщение Telegram.
    :param data_from_user: данные, собранные от пользователя.
    """
    if data_from_user.get('command') == '/bestdeal':
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": data_from_user['city_id']},
            "checkInDate": {
                'day': int(data_from_user['start_day']),
                'month': int(data_from_user['start_month']),
                'year': int(data_from_user['start_year'])
            },
            "checkOutDate": {
                'day': int(data_from_user['end_day']),
                'month': int(data_from_user['end_month']),
                'year': int(data_from_user['end_year'])
            },
            "rooms": [{"adults": 2}],
            "resultsStartingIndex": 0,
            "resultsSize": 30,
            "sort": "DISTANCE",
            "filters": {"price": {
                "max": data_from_user['max_price'],
                "min": data_from_user['min_price']
            }}
        }
    else:
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": data_from_user['city_id']},
            "checkInDate": {
                'day': int(data_from_user['start_day']),
                'month': int(data_from_user['start_month']),
                'year': int(data_from_user['start_year'])
            },
            "checkOutDate": {
                'day': int(data_from_user['end_day']),
                'month': int(data_from_user['end_month']),
                'year': int(data_from_user['end_year'])
            },
            "rooms": [{"adults": 2}],
            "resultsStartingIndex": 0,
            "resultsSize": 30,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
        }

    hotels_response = api_request(
        'POST',
        url='https://hotels4.p.rapidapi.com/properties/v2/list',
        querystring=payload
    )
    hotels = json.loads(hotels_response.text)
    hotels_data = {}
    for hotel in hotels['data']['propertySearch']['properties']:
        try:
            hotels_data[hotel['id']] = {
                'name': hotel['name'],
                'id': hotel['id'],
                'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
                'price': hotel['price']['lead']['amount']
            }
        except (KeyError, TypeError):
            continue
    # Сортируем по цене (от высокой стоимости к меньшей).
    if data_from_user['command'] == '/highprice':
        hotels_data = {
            key: value for key, value in
            sorted(hotels_data.items(), key=lambda hotel_id: hotel_id[1]['price'], reverse=True)
        }
    # Обнуляем созданный ранее словарь и добавляем туда только те отели, которые соответствуют диапазону.
    elif data_from_user['command'] == '/bestdeal':
        hotels_data = {}
        for hotel in hotels['data']['propertySearch']["properties"]:
            if data_from_user['start_distance'] < \
                    hotel['destinationInfo']['distanceFromDestination']['value'] < \
                    data_from_user['end_distance']:
                hotels_data[hotel['id']] = {
                    'name': hotel['name'],
                    'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
                    'price': hotel['price']['lead']['amount']
                }
    count = 0
    for key, hotel in hotels_data.items():
        # Нужен дополнительный запрос, чтобы получить детальную информацию об отеле.
        # Цикл будет выполняться, пока не достигнет числа отелей, которое запросил пользователь.
        if count < data_from_user['amount_hotels']:
            count += 1
            detail_payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "propertyId": key
            }
            detail_url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
            get_details = api_request('POST', detail_url, detail_payload)
            details_hotel = json.loads(get_details.text)
            details_hotel_data = {
                'id': key,
                'name': hotels_data[key]['name'],
                'price': hotels_data[key]['price'],
                'distance': hotels_data[key]['distance'],
                'address': details_hotel['data']['propertyInfo']['summary']['location']['address']['addressLine'],
                'images': [
                    url['image']['url'] for url in details_hotel['data']['propertyInfo']['propertyGallery']['images']
                ]
            }
            amount_nights = int((data_from_user['end_date'] - data_from_user['start_date']).total_seconds() / 86400)
            hotel_info = print_hotel_info(details_hotel_data, amount_nights)
            if data_from_user['need_photo']:
                # сформируем рандомный список из ссылок на фотографии, т.к. фото много, а надо только 10
                try:
                    images_urls = [
                        details_hotel_data['images'][random.randint(0, len(details_hotel_data['images']) - 1)]
                        for _ in range(data_from_user['amount_photos'])
                    ]
                    details_hotel_data['images'] = images_urls
                except IndexError:
                    continue
                if images_urls:
                    # формируем MediaGroup с фотографиями и описанием отеля и посылаем в чат
                    images = [
                        InputMediaPhoto(media=url, caption=hotel_info) if index == 0 else InputMediaPhoto(media=url)
                        for index, url in enumerate(images_urls)
                    ]
                    save_results(details_hotel_data, data_from_user, amount_nights)
                    bot.send_media_group(message.chat.id, images)
            else:
                # если фото не нужны, то просто выводим данные об отеле
                save_results(details_hotel_data, data_from_user, amount_nights)
                bot.send_message(message.chat.id, hotel_info)
        else:
            break
