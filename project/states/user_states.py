from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    """
    Класс реализует состояние пользователя внутри сценария.
    Атрибуты заполняются во время опроса пользователя. Очищаются при каждой новой команде.

    Attributes:
        city (str): город, в котором ищем отели.
        city_id (str): id города, в котором ищем отели.
        amount_hotels (int): количество отелей.
        need_photo (bool): нужно ли загружать фото.
        amount_photos (int): количество фото.
        start_date (datetime.date): дата заезда в отель.
        end_date (datetime.date): дата выезда из отеля.
        min_price (int): минимальная цена за ночь.
        max_price (int): максимальная цена за ночь.
        start_distance (float): минимальная дистанция до центра города.
        end_distance (float): максимальная дистанция до центра города.
    """
    command = State()
    city = State()
    city_id = State()
    amount_hotels = State()
    need_photo = State()
    amount_photos = State()
    start_date = State()
    end_date = State()
    min_price = State()
    max_price = State()
    start_distance = State()
    end_distance = State()
