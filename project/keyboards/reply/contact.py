from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Отправить контакт", request_contact=True))
    return keyboard


# @bot.message_handler(state=UserInfoState.city)
# def get_city(message: Message) -> None:
#     bot.send_message(message.from_user.id,
#                      "Спасибо, записал. Теперь отправь свой номер, нажав на кнопку",
#                      reply_markup=request_contact())
#     bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data["city"] = message.text


# @bot.message_handler(content_types=["text", "contact"], state=UserInfoState.phone_number)
# def get_contact(message: Message) -> None:
#     if message.content_type == "contact":
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data["phone_number"] = message.contact.phone_number
#
#             text = f"Спасибо за предоставленную информацию!\n" \
#                    f"Ваши данные:\n" \
#                    f"Имя: {data['name']}\n" \
#                    f"Возраст: {data['age']}\n" \
#                    f"Страна: {data['country']}\n" \
#                    f"Город: {data['city']}\n" \
#                    f"Номер телефона: {data['phone_number']}"
#             bot.send_message(message.from_user.id, text)
#     else:
#         bot.send_message(message.from_user.id, "Чтобы отправить контактную информацию, нажми на кнопку!")
