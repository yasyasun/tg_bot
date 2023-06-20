from peewee import *

from config_data.config import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})


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
        from_user (int): уникальное id пользователя из таблицы 'users' для связки таблиц.
    """
    id = PrimaryKeyField(unique=True)
    date = DateField()
    command = CharField()
    city = CharField()
    start_date = DateField()
    end_date = DateField()
    from_user = ForeignKeyField(User)

    class Meta:
        db_table = 'histories'
        order_by = 'date'


class SearchResult(BaseModel):
    """
    Класс для создания таблицы 'results' в БД.

    Attributes:
        id (int): уникальный id результата.
        hotel_id (int): id отеля.
        name (str): название отеля.
        amount_nights (int): количество ночей.
        price (float): цена за 1 ночь в $.
        total_price (float): итоговая стоимость за N ночей в $.
        distance (float): расстояние до центра города.
        address (str): адрес отеля.
        need_photo (bool): нужно ли загружать фото (True или False).
        from_history (int): уникальное id истории из таблицы 'histories' для связки таблиц.
    """
    id = PrimaryKeyField(unique=True)
    hotel_id = IntegerField()
    name = CharField()
    amount_nights = IntegerField()
    price = DecimalField(decimal_places=2, auto_round=True)
    total_price = DecimalField(decimal_places=2, auto_round=True)
    distance = FloatField()
    address = CharField()
    need_photo = BooleanField()
    from_history = ForeignKeyField(History, on_delete='CASCADE')

    class Meta:
        db_table = 'results'
        order_by = 'price_per_night'


class Images(BaseModel):
    """
    Класс для создания таблицы 'images' в БД, если нужны пользователю.

    Attributes:
        url (str): адрес фото.
        from_result (int): уникальное id отеля из таблицы 'results' для связки таблиц
    """
    url = CharField()
    from_result = ForeignKeyField(SearchResult, on_delete='CASCADE')

    class Meta:
        db_table = 'images'
