from typing import Dict, Union, List

from loguru import logger
from telebot.types import Message

from database.models import db, User, History, SearchResult
from loader import bot


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
        user = (User
                .select()
                .where(User.name == data['user'])
                )
        History(
            date=data['date_time'],
            command=data['command'],
            city=data['city'],
            start_date=f"{data['start_day']}-{data['start_month']}-{data['start_year']}",
            end_date=f"{data['end_day']}-{data['end_month']}-{data['end_year']}",
            from_user=user.id
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
        user = (User
                .select()
                .where(User.name == data_request['user'])
                )
        history = (History
                   .select()
                   .where(History.date == data_request['date_time'] and
                          History.from_user == user.id)
                   .get()
                   )
        SearchResult(
            hotel_id=data_hotel['id'],
            hotel_name=data_hotel['name'],
            amount_nights=amount_nights,
            price_per_night=data_hotel['price'],
            total_price=data_hotel['price'] * amount_nights,
            distance_city_center=data_hotel['distance'],
            hotel_address=data_hotel['address'],
            need_photo=data_hotel['need_photo'],
            images=data_hotel['images'],
            from_date=history.id
        ).save()


@logger.catch
def show_history(user: str) -> Union[List, None]:
    """
    Функция вывода истории поиска пользователя.

    :param user: имя пользователя Telegram (username).
    :return: список с запросами поиска пользователя или None
    """
    with db:
        user = (User
                .select()
                .where(User.name == user)
                )
        histories = [history for history in History.select().where(History.from_user == user.id)]
        if histories:
            return histories
        else:
            return None


@logger.catch
def delete_history(message: Message, user: str) -> None:
    """
    Функция очистки истории поиска пользователя.

    :param message: сообщение
    :param user: имя пользователя Telegram (username)
    """
    with db:
        user = (User
                .select()
                .where(User.name == user)
                )
        for history in History.select().where(History.from_user == user.id):
            history_date = History.get(History.date == history.date)
            SearchResult.delete().where(SearchResult.from_date == history_date).execute()
            History.delete_instance(history)
    bot.send_message(message.chat.id,
                     f"👍 <b>История поиска очищена!</b>\n"
                     f"Введите команду!\n"
                     f"Например: <b>/help</b>", parse_mode="html")
