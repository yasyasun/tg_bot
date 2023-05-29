from handlers.custom_handlers.lowprice import lowprice
from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "lowprice":
        lowprice(call.message)
