from telegram import Update
from telegram.ext import CallbackContext
import logging
from util import rss

from datetime import time, datetime
from database import schema
from database.engine import session
from sqlalchemy.sql.expression import text


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def fetch_rss_feeds(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    # context.bot.send_message(job.context, text='Beep!')
    q = session.query(schema.Feed)
    for item in q:
        curr = rss.RssFeed(item.URL)
        for feed in curr.items:
            messageContent = "Title: " + feed.title + "\nDescription: " + feed.description + "\n" + feed.link
            # escapedMessage = messageContent.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace('-', '\\').replace('>', '\\').replace('.', '\\').replace('(', '\\').replace(')', '\\').replace('(', '\\').replace('=', '\\').replace('#', '\\')
            messageContent = messageContent.replace('<br', '').replace('/>', '')
            context.bot.send_message(job.context, text=messageContent) #, parse_mode='MarkdownV2')

    