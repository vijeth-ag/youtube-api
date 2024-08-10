import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, ForeignKey, Column, Integer, VARCHAR, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("mysql+pymysql://user:password@127.0.0.1:3306/youtube_api_db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Channel(Base):
    __tablename__ = "Channel"

    channel_id = Column("channel_id", VARCHAR(255), primary_key=True)
    channel_name = Column("channel_name", VARCHAR(255))
    channel_type = Column("channel_type", VARCHAR(255))
    channel_views = Column("channel_views", Integer)
    channel_desc = Column("channel_desc", String(300))
    channel_status = Column("channel_status", VARCHAR(255))


    def __init__(self, channel_id, channel_name, channel_type, channel_views, channel_desc, channel_status):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_type = channel_type
        self.channel_views = channel_views
        self.channel_desc = channel_desc
        self.channel_status = channel_status
    
    # def __repr__(self):
    #     return f"({self.channel_id} {self.channel_name})"


class Playlist(Base):
    __tablename__ = "Playlist"

    playlist_id = Column("playlist_id", VARCHAR(255), primary_key=True)
    channel_id = Column("channel_id", VARCHAR(255), ForeignKey("Channel.channel_id"))
    playlist_name = Column("playlist_name", VARCHAR(255))


    def __init__(self, playlist_id, channel_id, playlist_name):
        self.playlist_id = playlist_id
        self.channel_id = channel_id
        self.playlist_name = playlist_name

class Video(Base):
    __tablename__ = "Video"

    video_id = Column("video_id", VARCHAR(255), primary_key=True)
    playlist_id = Column("playlist_id", VARCHAR(255), ForeignKey("Playlist.playlist_id"))
    video_name = Column("video_name", VARCHAR(255))
    video_desc = Column("video_desc", String(500))
    published_date = Column("published_date", DATETIME)
   
    view_count = Column("view_count", Integer)
    like_count = Column("like_count", Integer)
    dislike_count = Column("dislike_count", Integer)
    favorite_count = Column("favorite_count", Integer)
    comment_count = Column("comment_count", Integer)
    duration = Column("duration",  Integer)
    thumbnail = Column("thumbnail", VARCHAR(255))
    caption_status = Column("caption_status", VARCHAR(255))

    def __init__(self, video_id, playlist_id, video_name, video_desc, published_date, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status):
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.video_name = video_name
        self.video_desc = video_desc
        self.published_date = published_date
        self.view_count = view_count
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.favorite_count = favorite_count
        self.comment_count = comment_count
        self.duration = duration
        self.thumbnail = thumbnail
        self.caption_status = caption_status
    

class Comment(Base):
    __tablename__ = "Comment"

    comment_id = Column("comment_id", VARCHAR(255), primary_key=True)
    video_id = Column("video_id", VARCHAR(255), ForeignKey("Video.video_id"))
    comment_text = Column("comment_text", String(255))
    comment_author = Column("comment_author", VARCHAR(255))
    comment_published_date = Column("comment_published_date", DATETIME)

    def __init__(self, comment_id, video_id, comment_text, comment_author,comment_published_date):
        self.comment_id = comment_id
        self.video_id = video_id
        self.comment_text = comment_text
        self.comment_author = comment_author
        self.comment_published_date = comment_published_date

def create_tables():    
    Base.metadata.create_all(bind=engine)

def insert_channel_details(channel_details):

    channel = Channel(channel_details['channel_id'], channel_details['channel_name'], channel_details['channel_type'], \
                    channel_details['channel_views'], channel_details['channel_description'], \
                    channel_details['channel_status'])
    session.add(channel)
    session.commit()

    
def insert_playlists_data(playlists_data):
    for playlist in playlists_data:
        playlist = Playlist(playlist['id'], playlist['snippet']['channelId'], playlist['snippet']['title'])
        session.add(playlist)
    session.commit()

def insert_videos_data(videos_data):
    for video in videos_data:
        video = Video(video['snippet']['resourceId']['videoId'], video['snippet']['playlistId'], video['snippet']['title'], video['snippet']['video_description'], \
                    video['snippet']['publishedAt'], video['view_count'], video['like_count'], \
                    video['dislike_count'], video['favorite_count'], video['comment_count'], \
                    video['duration'], video['thumbnail'], video['caption_status'])    
        session.add(video)
    session.commit()

def insert_comments_data(comments_data):
    for comment in comments_data:
        comment = Comment(comment['comment_id'], comment['video_id'], comment['comment_text'], \
                        comment['comment_author'], comment['comment_published_date'])
        session.add(comment)
    session.commit()


def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
