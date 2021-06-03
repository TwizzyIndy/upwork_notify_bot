from sqlalchemy.sql.expression import text
from telegram import Update
from telegram.ext import CallbackContext
from datetime import time, datetime
from database import schema
from database.engine import session
from util import rss

from .fetch_rss import fetch_rss_feeds

import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def add_rss(update: Update, context: CallbackContext) -> None:

    if len(context.args) == 1:
        res = session.query(schema.Feed).filter_by(Type="rss", URL=context.args[0]).first()
        FID = None
        if res is None:
            # check if url works
            feedParsed = None
            try:
                feedParsed = rss.RssFeed(context.args[0])
                newFeed = schema.Feed(
                    Title=feedParsed.title,
                    URL=context.args[0],
                    Type="rss"
                )
                session.add(newFeed)
                session.commit()
                FID = newFeed.FID

                newSubscription = schema.PSubscription(
                    UID=update.effective_user.id,
                    FID=FID,
                    LatestCheck=datetime.now()
                )
                session.add(newSubscription)
                session.commit()

                start_timed_rss(update=update, context=context)

            except Exception as e:
                print(e)
                context.bot.send_message(chat_id=update.effective_chat.id, text="There was a problem parsing your rss feed")
                return
        else:
            FID = res.FID
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Check your format")

def start_timed_rss(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    
    try:
        duration = 1
        if duration < 0:
            update.message.reply_text('Sorry duration must be greater than zero')
            return
        
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(fetch_rss_feeds, duration * 60, context=chat_id, name=str(chat_id))
        
        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        
        update.message.reply_text(text)

    except (IndexError, ValueError) as e:
        logger.error(e)

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True