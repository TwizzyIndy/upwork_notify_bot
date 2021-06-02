from telegram import Update
from telegram.ext import CallbackContext
from datetime import time, datetime
from database import schema
from database.engine import session

def start(update: Update, context: CallbackContext) -> None:
    """Sends help info
    """
    if session.query(schema.User.UID).filter_by(UID=update.effective_user.id).scalar() is not None:
        context.bot.send_message(chat_id=update.effective_user.id, text="Welcome back, " + update.effective_user.username)
    else:
        # update.message.reply_text('Upwork Notifier Bot\nUser /set <minutes> to set a timer')
        newUser = schema.User(UID=update.effective_user.id, ChatID=update.effective_chat.id, FeedTime=time(hour=7, minute=30))
        session.add(newUser)
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, " + update.effective_user.username + ", you have been registered to our platform.\nType /help to learn to use this bot.")
        print("New user " + update.effective_user.username)