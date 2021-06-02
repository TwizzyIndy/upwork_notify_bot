from telegram import Update
from telegram.ext import CallbackContext
import logging
from .fetch_rss import fetch_rss_feeds

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in minutes
        duration = int(context.args[0])
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
        update.message.reply_text('Usage: /set <minutes>')
        logger.error(e)


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True