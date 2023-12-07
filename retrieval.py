
import sqlite3
import json
import requests
import os
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials




def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createMasterTable(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS master (id INTEGER PRIMARY KEY, title TEXT UNIQUE, artist TEXT)''')
    conn.commit()


def insertBillboardSongs(conn, cur):
    tracks = get25(cur)
    for track in tracks:
        id = track[0]
        title = track[1]
        artist = track[2]
        cur.execute("INSERT OR IGNORE INTO master (id, title, artist) VALUES (?, ?, ?)", (id, title, artist))
    conn.commit()

def get25(cur):
    url = "https://billboard2.p.rapidapi.com/hot_100"

    # date of billboard chart
    querystring = {"date":"2023-12-06"}

    # gets api keys dict
    with open('secrets.json') as f:
            secrets = json.load(f)

    # top 100 song list
    response = requests.get(url, headers=secrets['billboard'], params=querystring)
    top100 = response.json()
    
    # finds last entry in db 
    cur.execute('SELECT MAX(id) FROM master')
    startRank = cur.fetchone()
    
    # if there are no entries, set to 1
    if startRank[0] is None:
        startRank = 1
    else:
        # fetchone return type is a tuple -> startRank[first_element_in_tuple] 
        startRank = startRank[0] + 1
    # creates a list starting at last recorded rank + 1, spanning for 25
    # * is used to unpack range, otherwise it would store [range(params)]
    rankRange = [*range(startRank, startRank + 25)]

    result = []
    for track in top100:
        trackStats = []
        rank = int(track['rank'])
        # adds 25 songs in rank range
        if rank in rankRange:
            title = track['title' ]
            title = title.replace("&#039;", "'")
            artist = track['artist']
            trackStats.append(rank)
            trackStats.append(title)
            trackStats.append(artist)
            result.append(trackStats)
    return result



def load_secrets():
   with open('secrets.json') as f:
       secrets = json.load(f)
   return secrets


#youtube function
def get_youtube_video_info(api_key, song_title_list):
   # Set up the YouTube Data API client


   youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


   result_list = []


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


         
           channel = video_info["channelTitle"]
           publish_date = video_info["publishedAt"]
           views = statistics.get("viewCount", "N/A")
           likes = statistics.get("likeCount", "N/A")
           comments = statistics.get("commentCount", "N/A")
           favorites = statistics.get("favoriteCount", "N/A")
           duration = content_details.get("duration", "N/A")
           category = video_info.get("categoryId", "N/A")
           description = video_info.get("description", "N/A")
           result_list.append((channel, publish_date, views, likes, comments, favorites, duration, category, description))


       except HttpError as e:
           print(f"\nAn error occurred for '{song_title}': {e}")
       except IndexError:
           print(f"\nNo videos found for the title '{song_title}'.")
   return result_list




#spotify function
def get_song_info(client_id, client_secret, song_title):


   # Initialize Spotipy client
   client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
   sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


   # Search for the given song title
   result = sp.search(q=song_title, limit=1)


   if result['tracks']['items']:
       track = result['tracks']['items'][0]


       # Extract relevant information about the song
       song_info = {
           #'Song Name': track['name'],
           #'Artist(s)': ', '.join([artist['name'] for artist in track['artists']]),
           'Album': track['album']['name'],
           'Release Date': track['album']['release_date'],
           'Popularity': track['popularity'],
           'Danceability': None,
           'Tempo': None
       }


       # Get audio features for the track
       track_id = track['id']
       features = sp.audio_features(track_id)
       if features:
           song_info['Danceability'] = features[0]['danceability']
           song_info['Tempo'] = features[0]['tempo']


       return song_info
   else:
       return None

# returns list of tuples[(id, title)]
def getSongTitles(cur):
    cur.execute("SELECT id, title FROM master")
    return cur.fetchall()
    

    

def main():


    #api key loading
    secrets = load_secrets()
    api_key = secrets['youtube']['api_key']
    client_id = secrets['spotify']['client_id']
    client_secret = secrets['spotify']['client_secret']

    cur, conn = setUpDatabase('database.db')
    #createMasterTable(conn, cur)
    #insertBillboardSongs(conn, cur)

    #list of rank as tuples -> [(rank(id), title), (id, title)...]
    song_titles = getSongTitles(cur) #need to be passed a list

   #youtube
    youtube_tuples_list = []
    youtube_tuples_list = get_youtube_video_info(api_key, song_titles) # stored as list of tuples
    #the list of tuples look like this [(channel, publish_date, views, likes, comments, favorites, duration, category, description)]
    #append this into database.. how
    


   #spotify
   #take same list of song_titles as the youtube function
    spotify_data = [] #list of song_info dictionaries
    for song_title in song_titles:
        song_info = get_song_info(song_title)
        spotify_data.append(song_info)
    #the inner dictionaries look like this {Album: value, Release Data: value, Popularity: value, Danceability: value, Tempo: value}
    #append spotify_data into database.. how


    

    
main()
    

# example data
# {'artist': 'Big Sean', 'title': 'Why Would I Stop?', 'last_week': '-', 'rank': '97', 'award': True, 'image': 'https://charts-static.billboard.com/img/2011/01/big-sean-obf-180x180.jpg', 'peak_position': '97', 'weeks_on_chart': '1'}, 
# {'artist': 'Nio Garcia x Anuel AA x Myke Towers x Brray x Juanka', 'title': 'La Jeepeta', 'last_week': '95', 'rank': '98', 'award': True, 'image': 'https://charts-static.billboard.com/img/2020/05/nio-garcia-hk8-la-jeepeta-l5s-180x180.jpg', 'peak_position': '93', 'weeks_on_chart': '5'}, 
# {'artist': 'Migos Featuring YoungBoy Never Broke Again', 'title': 'Need It', 'last_week': '88', 'rank': '99', 'award': False, 'image': 'https://charts-static.billboard.com/img/2020/06/migos-ca0-needit-mz7-180x180.jpg', 'peak_position': '62', 'weeks_on_chart': '15'}, 
# {'artist': 'Ariana Grande &amp; Justin Bieber', 'title': 'Stuck With U', 'last_week': '91', 'rank': '100', 'award': False, 'image': 'https://charts-static.billboard.com/img/2020/05/ariana-grande-da0-stuck-with-u-yqg-180x180.jpg', 'peak_position': '1', 'weeks_on_chart': '18'}]