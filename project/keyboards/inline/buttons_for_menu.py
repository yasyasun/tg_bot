from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    command_low_price = InlineKeyboardButton(text="Топ самых дешёвых отелей", callback_data="low_high_best")
    keyboard.add(command_low_price)
    command_high_price = InlineKeyboardButton(text="Топ самых дорогих отелей", callback_data="low_high_best")
    keyboard.add(command_high_price)
    command_best_deal = InlineKeyboardButton(text="Топ отелей, наиболее подходящих по цене и расположению от центра",
                                             callback_data="low_high_best")
    keyboard.add(command_best_deal)
    command_history = InlineKeyboardButton(text="История поиска отелей", callback_data="history")
    keyboard.add(command_history)
    return keyboard
