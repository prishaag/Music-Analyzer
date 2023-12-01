#Prisha's file (all work is done by Prisha)

import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import json



def get_youtube_video_info(api_key, song_title_list):
    # Set up the YouTube Data API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    for song_title in song_title_list:
        try:
            # Search for videos with the given song title
            search_response = youtube.search().list(
                q=song_title,
                part="id",
                type="video",
                maxResults=1  
            ).execute()

            # Extract video ID from the search response
            video_id = search_response["items"][0]["id"]["videoId"]

            # Get video details based on the extracted video ID
            video_response = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            # Extract relevant information from the video response
            video_info = video_response["items"][0]["snippet"]
            statistics = video_response["items"][0]["statistics"]

            title = video_info["title"]
            channel = video_info["channelTitle"]
            publish_date = video_info["publishedAt"]
            views = statistics.get("viewCount", "N/A")
            likes = statistics.get("likeCount", "N/A")
            # dislikes = statistics.get("dislikeCount", "N/A")

            print(f"\nTitle: {title}")
            print(f"Channel: {channel}")
            print(f"Publish Date: {publish_date}")
            print(f"Views: {views}")
            print(f"Likes: {likes}")
            # print(f"Dislikes: {dislikes}")

            # cur.execute('''DROP TABLE IF EXISTS youtube''')
            # cur.execute('''CREATE TABLE youtube (id INTEGER FOREIGN KEY, views TEXT UNIQUE, artist TEXT)''')

        except HttpError as e:
            print(f"\nAn error occurred for '{song_title}': {e}")
        except IndexError:
            print(f"\nNo videos found for the title '{song_title}'.")

def load_secrets():
    with open('secrets.json') as f:
        secrets = json.load(f)
    return secrets

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual YouTube API key
    secrets = load_secrets()
    api_key = secrets['youtube']['api_key']
    # Replace 'SONG_TITLES' with a list of song titles you want to search for
    song_titles = ["Despacito", "Rap God"]
    get_youtube_video_info(api_key, song_titles)
