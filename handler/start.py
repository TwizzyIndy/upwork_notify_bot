from telegram import Update
from telegram.ext import CallbackContext
from datetime import time, datetime
from database import schema
from database.engine import session

from .fetch_rss import fetch_rss_feeds
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Sends help info
    """
    if session.query(schema.User.UID).filter_by(UID=update.effective_user.id).scalar() is not None:
        context.bot.send_message(chat_id=update.effective_user.id, text="Welcome back, " + update.effective_user.username)
        start_timed_rss(update=update, context=context)
    else:
        # update.message.reply_text('Upwork Notifier Bot\nUser /set <minutes> to set a timer')
        newUser = schema.User(UID=update.effective_user.id, ChatID=update.effective_chat.id, FeedTime=time(hour=7, minute=30))
        session.add(newUser)
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, " + update.effective_user.username + ", you have been registered to our platform.\nType /help to learn to use this bot.")
        print("New user " + update.effective_user.username)

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