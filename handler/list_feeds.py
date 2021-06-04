from sqlalchemy.sql.expression import text
from telegram import Update
from telegram.ext import CallbackContext
from datetime import time, datetime
from database import schema
from database.engine import session
from util import rss

def list_feeds(update: Update, context: CallbackContext) -> None:
    """List feeds in db"""

    q = session.query(schema.Feed).filter_by(UID=update.effective_user.id)
    n = 0
    message_content = ""

    if q is not None:
        for item in q:
            message_content += str(n+1) + ". " + item.Title + "\n"
            n += 1
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message_content)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please /add rss link first.")