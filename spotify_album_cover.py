import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Your Spotify API Credentials
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_API_KEY")

# Load your dataset
df = pd.read_csv('data/spotify-2023.csv', encoding='ISO-8859-1')

# Set up Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover URL
def get_album_cover(track_name, artist_name):
    results = sp.search(q='artist:' + artist_name + ' track:' + track_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        album_url = items[0]['album']['images'][0]['url']  # Assuming the first image is the cover
        return album_url
    else:
        return None

# Applying the function to each row
df['album_cover_url'] = df.apply(lambda row: get_album_cover(row['track_name'], row['artist(s)_name']), axis=1)

# Save the updated DataFrame
df.to_csv('data/updated_spotify_2023.csv', index=False)
