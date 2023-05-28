from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def about_photo() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard
