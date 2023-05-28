from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# from handlers.custom_handlers.lowprice import lowprice
from loader import bot


def show_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    command_lowprice = InlineKeyboardButton(text="Топ самых дешёвых отелей", callback_data="lowprice")
    keyboard.add(command_lowprice)
    return keyboard


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "lowprice":
#         lowprice(call.message)
