#Abigail's file (all work is done by Abby)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

def get_song_info(client_id, client_secret, song_title):
    # Replace with your credentials
    client_id = client_id
    client_secret = client_secret

    # Initialize Spotipy client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for the given song title
    result = sp.search(q=song_title, limit=1)

    if result['tracks']['items']:
        track = result['tracks']['items'][0]

        # Extract relevant information about the song
        song_info = {
            'Song Name': track['name'],
            'Artist(s)': ', '.join([artist['name'] for artist in track['artists']]),
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

# Example usage:
song_title = "Rap God"  # Replace with the song you want to search for
song_info = get_song_info(song_title)
if song_info:
    for key, value in song_info.items():
        print(f"{key}: {value}")
else:
    print("Song not found.")


def load_secrets():
    with open('secrets.json') as f:
        secrets = json.load(f)
    return secrets

if __name__ == "__main__":
    secrets = load_secrets()
    client_id = secrets['spotify']['client_id']
    client_secret = secrets['spotify']['client_secret']
    
    song_titles = ["Despacito", "Rap God"]
    get_song_info(client_id, client_secret, song_titles[0])
    get_song_info(client_id, client_secret, song_titles[1])