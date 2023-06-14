from loguru import logger
from telebot.types import Message

from database.models import db, User


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
