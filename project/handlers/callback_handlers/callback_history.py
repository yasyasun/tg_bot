import re

from loguru import logger
from telebot.types import CallbackQuery, InputMediaPhoto

from database.db_handlers import show_history, delete_history
from database.models import db, SearchResult, Images
from keyboards.inline.create_buttons import print_histories
from loader import bot
from utils.factories import for_history
from utils.get_hotels import print_hotel_info


@bot.callback_query_handler(func=lambda call: call.data == 'show_history' or call.data == 'delete_history')
@logger.catch
def process_history_reply(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие кнопки с выбором действия.
    В зависимости он нажатой кнопки вызывает нужную функцию:
    'Показать историю поиска' или 'Очистить историю'.
    Если выбрана кнопка 'Показать историю поиска' и есть рузельтат посика -
    предлагает пользователю инлайн-клавиатуру с его прошлыми запросами из таблицы 'histories'.

    :param call: отклик клавиатуры.
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data == "show_history":
            try:
                user_histories = show_history(username=data['user'])
                if user_histories:
                    bot.send_message(call.message.chat.id, text='Ваши прошлые запросы, выбирайте:',
                                     reply_markup=print_histories(user_histories))
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Ваша история пуста!</b>\nВведите какую-нибудь команду!\n"
                                     f"Например: <b>/help</b>", parse_mode="html")
            except Exception:
                bot.send_message(call.message.chat.id, text='⚠️Упс... ошибка: не могу загрузить историю поиска')
        elif call.data == "delete_history":
            try:
                delete_history(call.message, username=data['user'])
            except Exception:
                bot.send_message(call.message.chat.id, text='⚠️Упс... ошибка: не могу удалить историю поиска')
    bot.delete_state(call.message.chat.id)


@bot.callback_query_handler(func=None, history_config=for_history.filter())
@logger.catch
def clarify_history(call: CallbackQuery) -> None:
    """
    Функция ловит нажатие кнопки с выбором старых запросов, формирует результат из БД в список.

    :param call: отклик клавиатуры.
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    history_id = int(re.search(r'\d+', call.data).group())
    with db:
        results = [result for result in SearchResult.select().where(SearchResult.from_history == history_id)]
        for result in results:
            hotel_data = {
                'name': result.name,
                'distance': result.distance,
                'price': result.price,
                'total_price': result.total_price,
                'address': result.address,
                'need_photo': result.need_photo
            }
            hotel_info = print_hotel_info(hotel_data=hotel_data, amount_nights=result.amount_nights)
            if hotel_data['need_photo']:
                urls_images = [url.url for url in Images.select().where(Images.from_result == result.id)]
                images = [
                    InputMediaPhoto(media=url, caption=hotel_info) if index == 0 else InputMediaPhoto(media=url)
                    for index, url in enumerate(urls_images)
                ]
                bot.send_media_group(call.message.chat.id, images)
            else:
                bot.send_message(call.message.chat.id, hotel_info)
