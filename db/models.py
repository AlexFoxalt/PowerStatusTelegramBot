from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    home = Column(String, nullable=True)
    flat = Column(Integer, nullable=True)
    news_subscribed = Column(Boolean, default=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    children = relationship("Message", cascade="all,delete")


class Message(Base):
    __tablename__ = "messages"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.tg_id"))
    message = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Light(Base):
    __tablename__ = "light"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    value = Column(Boolean)
    mins_from_prev = Column(SmallInteger)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class PinnedMessage(Base):
    __tablename__ = "pinned"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True)
    text = Column(String, default="Default message", nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
