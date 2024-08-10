from .tables import create_tables

def init_db():
    print("initting DB===================")
    create_tables()


def insert_channel_details(channel_id, channel_details):
    channel = Channel(channel_id, channel_details['title'], channel_details['description'], channel_details['published_at'], channel_details['subscriber_count'], channel_details['view_count'], channel_details['video_count'])
    