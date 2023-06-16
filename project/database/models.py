from peewee import *

db = SqliteDatabase('search_history.db')


class BaseModel(Model):
    """ Базовый класс для создания таблиц в БД. """

    class Meta:
        database = db


class User(BaseModel):
    """
    Класс для создания таблицы 'users' в БД.

    Attributes:
        name (str): уникальное имя пользователя (сюда запишется username пользователя Telegram).
    """

    name = CharField(unique=True)

    class Meta:
        db_table = 'users'
        order_by = 'id'


class History(BaseModel):
    """
    Класс для создания таблицы 'histories' в БД.

    Attributes:
        date (datetime.date): дата запроса пользователя.
        command (str): команда запроса ('/lowprice', '/highprice', '/bestdeal').
        city (str): город.
        start_date (datetime.date): дата заселения в отель.
        end_date (datetime.date): дата выселения из отеля.
        from_user (str): name - уникальное имя пользователя из таблицы 'users' для связки таблиц.
    """
    date = DateField()
    command = CharField()
    city = CharField()
    start_date = DateField()
    end_date = DateField()
    from_user = ForeignKeyField(User.name, backref='history')

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
        from_date (datetime.date): date - уникальная дата запроса из таблицы 'histories' для связки таблиц.
    """
    hotel_id = IntegerField()
    hotel_name = CharField()
    amount_nights = IntegerField()
    price_per_night = DecimalField(decimal_places=1)
    total_price = DecimalField(decimal_places=1)
    distance_city_center = FloatField()
    hotel_address = CharField()
    from_date = ForeignKeyField(History.date)

    class Meta:
        db_table = 'results'
        order_by = 'price_per_night'
