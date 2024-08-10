import json
from googleapiclient.discovery import build


# Replace with your API key
API_KEY = 'AIz'

# Create a service object
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_details(channel_id):
    channel_data = {}

    try:

        # fetch the channel details
        request = youtube.channels().list(
            part='snippet,contentDetails,statistics,topicDetails,status,brandingSettings',
            id=channel_id
        )
        channel_response = request.execute()

        channel_info = channel_response.get('items', [])[0]

        channel_details = {
            'channel_id': channel_info['id'],
            'channel_name': channel_info['snippet']['title'],
            'channel_type': channel_info['kind'],
            'channel_views': channel_info['statistics'].get('viewCount', 'N/A'),
            'channel_description': channel_info['snippet']['description'],
            'channel_status': channel_info['status'].get('privacyStatus', 'N/A'),
        }
        channel_data["channel_details"] = channel_details

        uploads_playlist_id = channel_info['contentDetails']['relatedPlaylists']['uploads']

        request = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10  # Number of videos to retrieve, can be adjusted
        )
        response = request.execute()

        playlists_data = response.get('items', [])
        channel_data["playlists_data"] = playlists_data


        # Fetch videos from the uploads playlist
        request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=50  # Number of videos to retrieve, can be adjusted
        )
        response = request.execute()
        response_data = response.get('items', [])
        channel_data["videos"] = response_data

        for video in response_data:
            video_id = video['snippet']['resourceId']['videoId']
            comment_request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50  # Number of comments to retrieve, can be adjusted
            )
            comment_response = comment_request.execute()
            comment_data = comment_response.get('items', [])
            channel_data["comment_data"] = comment_data

        return channel_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

