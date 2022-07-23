from sqlalchemy.sql.expression import text
from telegram import Update
from telegram.ext import CallbackContext
from datetime import time, datetime
from database import schema
from database.engine import engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from util import rss

from .fetch_rss import fetch_rss_feeds

import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

session = scoped_session( sessionmaker(bind=engine) )

def remove_rss(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1:
        res = session.query(schema.Feed).filter_by(Type="rss", FID=context.args[0]).first()

        if res:
            try:
                session.delete(res)
                session.commit()
            except Exception as e:
                print(e)
                context.bot.send_message(chat_id=update.effective_chat.id, text="There was a problem removing your rss feed")
                return
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Put list ID")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Check your format")