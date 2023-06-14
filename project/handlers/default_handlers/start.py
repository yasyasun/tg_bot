from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.username}!\n"
                                           f"Можете ввести какую-нибудь команду!\n"
                                           f"Например: <b>/help</b>", parse_mode='html')
