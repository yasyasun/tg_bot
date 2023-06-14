from handlers.custom_handlers.input_data import low_high_best_handler
from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def menu_callback(call):
    if call.data == "low_high_best":
        low_high_best_handler(call)
