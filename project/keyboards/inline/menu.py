from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    command_lowprice = InlineKeyboardButton(text="Топ самых дешёвых отелей", callback_data="lowprice")
    keyboard.add(command_lowprice)
    return keyboard
