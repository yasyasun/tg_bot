from telebot.handler_backends import State, StatesGroup


class UserChoiceState(StatesGroup):
    city = State()
    amt_hotels = State()
    photo_need_or_not = State()
    amt_photos = State()
