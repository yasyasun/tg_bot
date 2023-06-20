from telebot import AdvancedCustomFilter
from telebot.callback_data import CallbackDataFilter
from telebot.types import CallbackQuery


class HistoryCallbackFilter(AdvancedCustomFilter):
    """ Фильтр для клавиатуры с выбором истории поиска """

    key = 'history_config'

    def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)
