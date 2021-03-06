import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from handler.start import start
from handler.set_timer import set_timer
from handler.fetch_rss import fetch_rss_feeds
from handler.unset_timer import unset
from handler.add_rss import add_rss
from handler.remove_rss import remove_rss
from handler.list_feeds import list_feeds
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# PORT = os.environ.get('PORT')
TOKEN = "PLEASE_USE_UNIQUE_TOKEN_HERE"

def main() -> None:
    """Run bot"""

    updater = Updater(TOKEN)#, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    dispatcher.add_handler(CommandHandler("add", add_rss))
    dispatcher.add_handler(CommandHandler("remove", remove_rss))
    dispatcher.add_handler(CommandHandler("list", list_feeds))
    
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()