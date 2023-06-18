from peewee import *

from config_data.config import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    """ Базовый класс для создания таблиц в БД. """

    class Meta:
        database = db


class User(BaseModel):
    """
    Класс для создания таблицы 'users' в БД.

    Attributes:
        id (int): уникальный id пользователя.
        name (str): уникальное имя пользователя (сюда запишется username пользователя Telegram).
    """
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)

    class Meta:
        db_table = 'users'
        order_by = 'id'


class History(BaseModel):
    """
    Класс для создания таблицы 'histories' в БД.

    Attributes:
        id (int): уникальный id истории.
        date (datetime.date): дата запроса пользователя.
        command (str): команда запроса ('/lowprice', '/highprice', '/bestdeal').
        city (str): город.
        start_date (datetime.date): дата заселения в отель.
        end_date (datetime.date): дата выселения из отеля.
        from_user (str): name - уникальное имя пользователя из таблицы 'users' для связки таблиц.
    """
    id = PrimaryKeyField(unique=True)
    date = DateField()
    command = CharField()
    city = CharField()
    start_date = DateField()
    end_date = DateField()
    from_user = ForeignKeyField(User, backref='history')

    class Meta:
        db_table = 'histories'
        order_by = 'date'


class SearchResult(BaseModel):
    """
    Класс для создания таблицы 'results' в БД.

    Attributes:
        hotel_id (int): id отеля.
        hotel_name (str): название отеля.
        amount_nights (int): количество ночей.
        price_per_night (float): цена за 1 ночь в $.
        total_price (float): итоговая стоимость за N ночей в $.
        distance_city_center (float): расстояние до центра города.
        hotel_address (str): адрес отеля.
        need_photo (bool): нужно ли загружать фото (True или False).
        images (str): адреса фото, если нужны.
        from_date (datetime.date): date - уникальная дата запроса из таблицы 'histories' для связки таблиц.
    """
    hotel_id = IntegerField()
    hotel_name = CharField()
    amount_nights = IntegerField()
    price_per_night = DecimalField(decimal_places=1)
    total_price = DecimalField(decimal_places=1)
    distance_city_center = FloatField()
    hotel_address = CharField()
    need_photo = BooleanField()
    images = CharField(default='')
    from_date = ForeignKeyField(History, backref='result')

    class Meta:
        db_table = 'results'
        order_by = 'price_per_night'
