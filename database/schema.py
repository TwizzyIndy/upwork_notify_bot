from sqlalchemy import Column, Integer, String, Time, Date, Sequence, ForeignKey, Enum, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Feed(Base):
    __tablename__ = 'feeds'
    FID = Column(Integer, Sequence('feed_id_seq'), primary_key=True)
    Title = Column(String, nullable=False)
    URL = Column(String, unique=True, nullable=False)
    Type = Column(Enum("rss", "podcast"), nullable=False)


class PSubscription(Base):
    __tablename__ = 'psubscriptions'
    SID = Column(Integer, Sequence('psub_id_seq'), primary_key=True)
    UID = Column(Integer, ForeignKey('users.UID'), nullable=False)
    FID = Column(Integer, ForeignKey('feeds.FID'), nullable=False)
    LatestCheck = Column(Date, nullable=False)

    user = relationship("User", back_populates="subscriptions")
    feed = relationship("Feed")

    Death = Column(Boolean)


class User(Base):
    __tablename__ = 'users'
    UID = Column(Integer, primary_key=True)
    ChatID = Column(Integer, unique=True, nullable=False)
    FeedTime = Column(Time, nullable=False)

    subscriptions = relationship("PSubscription", order_by=PSubscription.FID)