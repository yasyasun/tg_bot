from keyboards.reply.contact import request_contact
from keyboards.reply.photo import about_photo
from loader import bot
from states.user_choice import UserChoiceState
from telebot.types import Message


@bot.message_handler(commands=["lowprice"])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserChoiceState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите город поиска")


@bot.message_handler(state=UserChoiceState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо! Введите количество отелей")
        bot.set_state(message.from_user.id, UserChoiceState.amt_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["city"] = message.text

    else:
        bot.send_message(message.from_user.id, "Город может содержать только буквы!")


@bot.message_handler(state=UserChoiceState.amt_hotels)
def get_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Спасибо! Вам нужны фотографии?", reply_markup=about_photo())
        bot.set_state(message.from_user.id, UserChoiceState.photo_need_or_not, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["amt_hotels"] = message.text

    else:
        bot.send_message(message.from_user.id, "Введите число!")


@bot.message_handler(state=UserChoiceState.photo_need_or_not)
def get_photo(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, "Спасибо! Введите количество фотографий")
        bot.set_state(message.from_user.id, UserChoiceState.amt_photos, message.chat.id)

    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, "Спасибо за запрос!")

    else:
        bot.send_message(message.from_user.id, "Выберите Да или Нет!")


@bot.message_handler(state=UserChoiceState.amt_photos)
def get_photos(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Спасибо за запрос!")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["amt_photos"] = message.text

    else:
        bot.send_message(message.from_user.id, "Введите число!")
