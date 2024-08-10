from datetime import datetime
import pymysql
import re
import pandas as pd

from sqlalchemy import func, extract


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
    favorite_count = Column("favorite_count", Integer)
    comment_count = Column("comment_count", Integer)
    duration = Column("duration",  VARCHAR(255))
    thumbnail = Column("thumbnail", VARCHAR(255))
    caption_status = Column("caption_status", VARCHAR(255))

    def __init__(self, video_id, playlist_id, video_name, video_desc, published_date, view_count, like_count, favorite_count, comment_count, duration, thumbnail, caption_status):
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.video_name = video_name
        self.video_desc = video_desc
        self.published_date = published_date
        self.view_count = view_count
        self.like_count = like_count
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
        print("playlist------------------",playlist)

        playlist = Playlist(playlist['id'], playlist['snippet']['channelId'], playlist['snippet']['title'])
        session.add(playlist)
    session.commit()

def insert_videos_data(videos_data):
    for video in videos_data:
        sql_datetime_str = video['snippet']['publishedAt'].replace('T', ' ').replace('Z', '')
        parsed_datetime = datetime.strptime(sql_datetime_str, '%Y-%m-%d %H:%M:%S')

        video = Video(video['snippet']['resourceId']['videoId'], video['snippet']['playlistId'], video['snippet']['title'], \
                    video['snippet']['description'], \
                    parsed_datetime, video['statistics']['viewCount'], video['statistics']['likeCount'], \
                    video['statistics']['favoriteCount'], video['statistics']['commentCount'], \
                    video['contentDetails']['duration'], video['snippet']['thumbnails']['default']['url'], video['contentDetails']['caption'])    
        session.add(video)
    session.commit()

def insert_comments_data(comments_data):
    for comment in comments_data:
        comment_published_date = datetime.strptime(comment['snippet']['topLevelComment']['snippet']['publishedAt'].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')

        comment = Comment(comment['id'], comment['snippet']['videoId'], comment['snippet']['topLevelComment']['snippet']['textOriginal'], \
                        comment['snippet']['topLevelComment']['snippet']['authorDisplayName'], comment_published_date)
        session.add(comment)
    session.commit()



# Queryies
def get_vidoos_and_channel():
    results = session.query(Video.video_name, Channel.channel_name)\
    .join(Playlist, Video.playlist_id == Playlist.playlist_id)\
    .join(Channel, Playlist.channel_id == Channel.channel_id)\
    .all()

    return results

def most_videos():
    results = session.query(Channel.channel_name, func.count(Video.video_id).label('video_count'))\
        .join(Playlist, Channel.channel_id == Playlist.channel_id)\
        .join(Video, Playlist.playlist_id == Video.playlist_id)\
        .group_by(Channel.channel_id)\
        .order_by(func.count(Video.video_id).desc())\
        .all()
    return results


def top_10():
    results = session.query(
        Video.video_name,
        Channel.channel_name,
        Video.view_count
    ).join(
        Playlist, Video.playlist_id == Playlist.playlist_id
    ).join(
        Channel, Playlist.channel_id == Channel.channel_id
    ).order_by(
        Video.view_count.desc()
    ).limit(10).all()
    return results

def comments_video_names():
    results = session.query(
        Video.video_name,
        func.count(Comment.comment_id).label('comment_count')
    ).outerjoin(
        Comment, Video.video_id == Comment.video_id
    ).group_by(
        Video.video_id
    ).all()
    return results


def highest_likes():
    results = session.query(
        Video.video_name,
        Channel.channel_name,
        Video.like_count
    ).join(
        Playlist, Video.playlist_id == Playlist.playlist_id
    ).join(
        Channel, Playlist.channel_id == Channel.channel_id
    ).order_by(
        Video.like_count.desc()
    ).all()

    return results

def total_likes():
    results = session.query(
        Video.video_name,
        Video.like_count
    ).all()
    return results


def total_views_channel_names():
    results = session.query(
        Channel.channel_name,
        func.sum(Video.view_count).label('total_views')
    ).join(
        Playlist, Channel.channel_id == Playlist.channel_id
    ).join(
        Video, Playlist.playlist_id == Video.playlist_id
    ).group_by(
        Channel.channel_id
    ).all()
    return results

def videos_2022():
    results = session.query(
        Channel.channel_name
    ).join(
        Playlist, Channel.channel_id == Playlist.channel_id
    ).join(
        Video, Playlist.playlist_id == Video.playlist_id
    ).filter(
        extract('year', Video.published_date) == 2022
    ).distinct().all()
    return results

def avg_duration():
    results = session.query(
        Channel.channel_name,
        Video.duration
    ).join(
        Playlist, Video.playlist_id == Playlist.playlist_id
    ).join(
        Channel, Playlist.channel_id == Channel.channel_id
    ).all()

    data = [(channel_name, iso8601_duration_to_seconds(duration)) for channel_name, duration in results]
    df = pd.DataFrame(data, columns=['channel_name', 'duration_seconds'])

    # Calculate average duration per channel
    average_durations = df.groupby('channel_name')['duration_seconds'].mean().reset_index()
    average_durations['average_duration'] = pd.to_timedelta(average_durations['duration_seconds'], unit='s')

    return average_durations

def highest_comments_channel_name():
    results = session.query(
        Video.video_name,
        Channel.channel_name,
        func.count(Comment.comment_id).label('comment_count')
    ).join(
        Playlist, Video.playlist_id == Playlist.playlist_id
    ).join(
        Channel, Playlist.channel_id == Channel.channel_id
    ).outerjoin(
        Comment, Video.video_id == Comment.video_id
    ).group_by(
        Video.video_id,
        Channel.channel_name
    ).order_by(
        func.count(Comment.comment_id).desc()
    ).all()

    return results


def iso8601_duration_to_seconds(duration):
    matches = re.findall(r'(\d+)([HMSS])', duration)
    total_seconds = 0
    for value, unit in matches:
        if unit == 'H':
            total_seconds += int(value) * 3600
        elif unit == 'M':
            total_seconds += int(value) * 60
        elif unit == 'S':
            total_seconds += int(value)
    return total_seconds

def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
