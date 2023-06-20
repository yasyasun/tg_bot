from typing import Dict, Union, List

from loguru import logger
from telebot.types import Message

from database.models import db, User, History, SearchResult, Images
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
                .get()
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
                .get()
                )
        history = (History
                   .select()
                   .where(History.from_user == user.id and History.date == data_request['date_time'])
                   .get()
                   )
        SearchResult(
            hotel_id=data_hotel['id'],
            name=data_hotel['name'],
            amount_nights=amount_nights,
            price=data_hotel['price'],
            total_price=data_hotel['price'] * amount_nights,
            distance=data_hotel['distance'],
            address=data_hotel['address'],
            need_photo=data_hotel['need_photo'],
            from_history=history.id
        ).save()


@logger.catch
def save_images(url: str, id_hotel: int):
    """
    Функция для сохранения фотографий отеля в БД.
    Забирает данные и сохраняет в таблицу 'images'.

    :param url: словарь с информацией по отелю.
    :param id_hotel: словарь со всеми данными запроса.
    """
    with db:
        result = (SearchResult
                  .select()
                  .where(SearchResult.hotel_id == id_hotel)
                  .get()
                  )
        Images(
            url=url,
            from_result=result.id
        ).save()


@logger.catch
def show_history(username: str) -> Union[List, None]:
    """
    Функция вывода истории поиска пользователя.
    Проверяет наличие истории поиска в БД.


    :param username: имя пользователя Telegram (username).
    :return: список с запросами поиска пользователя или None
    """
    with db:
        user = (User
                .select()
                .where(User.name == username)
                .get()
                )
        histories = [history for history in History.select().where(History.from_user == user.id)]
        if histories:
            return histories
        else:
            return None


@logger.catch
def delete_history(message: Message, username: str) -> None:
    """
    Функция очистки истории поиска пользователя.

    :param message: сообщение
    :param username: имя пользователя Telegram (username)
    """
    with db:
        user = (User
                .select()
                .where(User.name == username)
                .get()
                )
        for history in History.select().where(History.from_user == user.id):
            History.delete_instance(history)
    bot.send_message(message.chat.id,
                     f"👍 <b>История поиска очищена!</b>\n"
                     f"Введите команду!\n"
                     f"Например: <b>/help</b>", parse_mode="html")
