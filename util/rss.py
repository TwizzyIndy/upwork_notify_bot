import atoma
from requests import get
from util._article import Article, Feed

class RssArticle(Article):
    def send(self, ChatID, bot):
        messageContent = "*" + self.title + "*\n" + self.description + "\n" + self.link
        bot.sendMessage(chat_id=ChatID, text=messageContent, parse_mode='MarkdownV2')


class RssFeed(Feed):
    def __init__(self, link):
        super().__init__()
        xml = get(link)
        feed = atoma.parse_rss_bytes(xml.content)
        self.title = feed.title
        for item in feed.items:
           self.items.append(RssArticle(item.title, item.description, item.link, item.pub_date))
        self.items.reverse()