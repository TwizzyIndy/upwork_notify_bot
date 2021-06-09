from sqlalchemy.orm.session import sessionmaker
from telegram import Update
from telegram.ext import CallbackContext
import logging

from telegram.utils.helpers import escape_markdown
from util import rss

from datetime import time, datetime
from database import schema
from database.engine import engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql.expression import text

from markdownify import markdownify as md

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

session = scoped_session( sessionmaker(bind=engine) )

def fetch_rss_feeds(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    # context.bot.send_message(job.context, text='Beep!')
    q = session.query(schema.Feed).filter_by(UID=job.name)

    if q.count() == 0:
        context.bot.send_message(job.context, text="Please /add rss link first.")
        return None
    
    for item in q:
        curr = rss.RssFeed(item.URL)
        for feed in curr.items:
            
            if session.query(schema.News.title).filter_by(title=feed.title, UID=job.name, FID=item.FID).scalar() is None:
                
                save_news_to_db(feed.title, feed.link, feed.pub_date, job_name=job.name, fid=item.FID)
                description = md(feed.description).replace('**', '*')
                messageContent = "*Title* : " + escape_markdown( feed.title.replace(' - Upwork','') )+ "\n*Description* : " + description

                try:
                    context.bot.send_message(job.context, text=messageContent, parse_mode='Markdown')
                except Exception as e:
                    print(e)
                    messageContent = "*Title* : " + escape_markdown( feed.title.replace(' - Upwork','') )+ "\n*Description* : " + escape_markdown( description )
                    context.bot.send_message(job.context, text=messageContent, parse_mode='Markdown')
                    continue


def save_news_to_db(title, link, pubdate, job_name, fid):

    newRssItem = schema.News(title=title, link=link, pubdate=pubdate, UID=job_name, FID=fid)
    session.add(newRssItem)
    session.commit()
    return
    