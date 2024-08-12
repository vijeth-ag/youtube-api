import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = os.getenv('YOUTUBE_API_KEY')

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
        upload_playlist_data = {
            'id': uploads_playlist_id,
            'snippet': {
                'channelId': channel_id,
                'title': 'Uploads'                
            }
        }

        playlists_data.append(upload_playlist_data)

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
            video_details_request = youtube.videos().list(
                part='statistics,contentDetails',
                id=video_id
            )
            video_details_response = video_details_request.execute()
            video_details = video_details_response.get('items', [])[0]

            # if  video_details['statistics']['commentCount'] is null or not exists assign 0
            if 'commentCount' not in video_details['statistics']:
                video_details['statistics']['commentCount'] = 0

            video["statistics"] = video_details['statistics']
            video["contentDetails"] = video_details['contentDetails']

            comment_response = get_comments(video_id)

            comment_data = comment_response.get('items', [])
            channel_data["comment_data"] = comment_data

        return channel_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_comments(video_id):
    try:
        # Make the request to the YouTube API
        comment_request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50  # Number of comments to retrieve, can be adjusted
        )
        response = comment_request.execute()
        return response

    except HttpError as error:
        error_content = error.content.decode('utf-8')
        
        # Check if comments are disabled for the video
        if 'commentsDisabled' in error_content:
            return {
                "items": [empty_comment_thread]
            }

        else:
            # Handle other types of errors
            print(f"An error occurred: {error}")
            # return None  # or handle accordingly
            return {
                "items": [empty_comment_thread]
            }


empty_comment_thread = {
    "kind": "",
    "etag": "",
    "id": "",
    "snippet": {
        "channelId": "",
        "videoId": "",
        "topLevelComment": {
            "kind": "",
            "etag": "",
            "id": "",
            "snippet": {
                "channelId": "",
                "videoId": "",
                "textDisplay": "",
                "textOriginal": "",
                "authorDisplayName": "",
                "authorProfileImageUrl": "",
                "authorChannelUrl": "",
                "authorChannelId": {
                    "value": ""
                },
                "canRate": False,
                "viewerRating": "",
                "likeCount": 0,
                "publishedAt": "",
                "updatedAt": ""
            }
        },
        "canReply": False,
        "totalReplyCount": 0,
        "isPublic": False
    }
}
