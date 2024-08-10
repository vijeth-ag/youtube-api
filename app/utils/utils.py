import re
from urllib.parse import urlparse


def is_valid_youtube_channel_url(url):
    # channel_url_patterns = [
    #     r'^https?:\/\/(www\.)?youtube\.com\/@[A-Za-z0-9_-]+$',
    #     r'^https?:\/\/(www\.)?youtube\.com\/channel\/[A-Za-z0-9_-]+$',
    #     r'^https?:\/\/(www\.)?youtube\.com\/c\/[A-Za-z0-9_-]+$',
    #     r'^https?:\/\/(www\.)?youtube\.com\/user\/[A-Za-z0-9_-]+$'
    # ]

    channel_url_patterns = [
        r'youtube\.com\/@[A-Za-z0-9_-]+$',
        r'youtube\.com\/channel\/[A-Za-z0-9_-]+$',
        r'youtube\.com\/c\/[A-Za-z0-9_-]+$',
        r'youtube\.com\/user\/[A-Za-z0-9_-]+$'
    ]


    for pattern in channel_url_patterns:
        if re.match(pattern, url):
            return True
    return False

def get_channelid_from_url(url):
    tokens = url.split("/")

    print("tokens",tokens)
    print("tokens len",len(tokens)-1)
    return tokens[len(tokens)-1]


    # if "youtube.com/channel" in url:
    #     print("youtube.com/channel type")        
    # elif "youtube.com/c" in url:
    #     print("youtube.com/c type")
    # elif "youtube.com/@" in url:
    #     print("youtube.com/c type")
    # elif "youtube.com/user" in url:
    #     print("youtube.com/c type")        