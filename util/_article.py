import datetime

class Article:
    def __init__(self, title, description, link, pub_date):
        self.title = title
        self.description = description
        self.link = link
        self.pub_date = pub_date

    def send(self, ChatID):
        print("You should implement this method yourself")

class Feed:
    def __init__(self):
        self.items = list()

    def sendUpdates(self, ChatID, bot, lastUpdate=datetime.date.fromtimestamp(0)):
        count = 0
        if any(item.pub_date > lastUpdate for item in self.items):
            bot.sendMessage(chat_id=ChatID, text="*"+self.title+"*", parse_mode='MarkdownV2')
            toBeSent = filter(lambda item: item.pub_date > lastUpdate, self.items)
            for item in toBeSent:
                item.send(ChatID, bot)