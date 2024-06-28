from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import database_url

DATABASE_URL = database_url
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    videos = relationship("Video", back_populates="channel")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    views = Column(Integer)
    link = Column(String, unique=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = relationship("Channel", back_populates="videos")


Base.metadata.create_all(bind=engine)
