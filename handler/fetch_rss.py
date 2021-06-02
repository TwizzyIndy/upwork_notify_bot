from telegram import Update
from telegram.ext import CallbackContext
import logging

from telegram.utils.helpers import escape_markdown
from util import rss

from datetime import time, datetime
from database import schema
from database.engine import session
from sqlalchemy.sql.expression import text

from markdownify import markdownify as md

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
            
            description = md(feed.description).replace('**', '*')
            messageContent = "*Title* : " + escape_markdown( feed.title )+ "\n*Description* : " + description

            try:
                context.bot.send_message(job.context, text=messageContent, parse_mode='Markdown')
            except Exception as e:
                print(e)
                messageContent = "*Title* : " + escape_markdown( feed.title )+ "\n*Description* : " + escape_markdown( description )
                context.bot.send_message(job.context, text=messageContent, parse_mode='Markdown')


    