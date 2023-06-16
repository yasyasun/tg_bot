from typing import Dict

from loguru import logger
from telebot.types import Message

from database.models import db, User, History, SearchResult


@logger.catch
def save_user(message: Message) -> None:
    """
    Функция сохранения имени пользователя.
    Проверяет наличие пользователя в БД, если его нет, заносит в БД в таблицу 'users'.

    :param message: сообщение Telegram.
    """
    with db:
        username = message.from_user.username
        try:
            user_id = User.get(User.name == username)
        except Exception:
            user_id = None
        if not user_id:
            User(name=username).save()


@logger.catch
def save_history(data: Dict) -> None:
    """
    Функция для сохранения истории поиска в БД.
    Забирает данные и сохраняет в таблицу 'histories'.

    :param data: словарь со всеми данными запроса.
    """
    with db:
        History(
            date=data['date_time'],
            command=data['command'],
            city=data['city'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            from_user=User.select('id').where(User.name == data['user'])
        ).save()


@logger.catch
def save_results(data_hotel: Dict, data_request: Dict, amount_nights: int) -> None:
    """
    Функция для сохранения истории поиска в БД.
    Забирает данные и сохраняет в таблицу 'results'.

    :param data_hotel: словарь с информацией по отелю.
    :param data_request: словарь со всеми данными запроса.
    :param amount_nights: количество ночей.
    """
    with db:
        SearchResult(
            hotel_id=data_hotel['id'],
            hotel_name=data_hotel['name'],
            amount_nights=amount_nights,
            price_per_night=data_hotel['price'],
            total_price=data_hotel['price'] * amount_nights,
            distance_city_center=data_hotel['distance'],
            hotel_address=data_hotel['address'],
            from_date=History.select().where(
                History.from_user == User.get(User.name == data_request['user']) and
                History.date == data_request['date_time']
            )
        ).save()
