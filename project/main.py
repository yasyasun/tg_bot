from database.models import db, User, History, SearchResult, Images
from keyboards.inline.filters import HistoryCallbackFilter
from loader import bot
import handlers  # noqa
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    with db:
        db.create_tables([User, History, SearchResult, Images])
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(HistoryCallbackFilter())
    set_default_commands(bot)
    bot.infinity_polling()
