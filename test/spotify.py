import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# read key-value pairs from a .env file and set them as environment variables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Spotify client with credentials from environment variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

if not client_id or not client_secret:
    raise ValueError("Missing Spotify credentials in .env file")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))


def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"


def print_artist_details(artist):
    """Print comprehensive artist information"""
    if not artist:
        print("Could not retrieve artist information")
        return

    print("🎵 ARTIST DETAILS")
    print("=" * 50)
    print(f"Name: {artist['name']}")
    print(f"Spotify ID: {artist['id']}")
    print(f"Popularity Score: {artist['popularity']}/100")
    print(f"Followers: {format_number(artist['followers']['total'])}")
    print(f"Spotify URL: {artist['external_urls']['spotify']}")

    if artist['images']:
        print(f"Profile Image: {artist['images'][0]['url']}")

    if artist['genres']:
        print(f"Genres: {', '.join(artist['genres'])}")

    # Estimate monthly listeners (based on popularity and followers)
    popularity = artist['popularity']
    followers = artist['followers']['total']

    # Rough estimation: monthly listeners ≈ followers * (popularity/100) * 0.3
    # This is an approximation since Spotify doesn't provide exact monthly listeners
    estimated_monthly_listeners = int(followers * (popularity / 100) * 0.3)
    print(
        f"Estimated Monthly Listeners: {format_number(estimated_monthly_listeners)}")

    print("\n📊 ADDITIONAL INFO")
    print("-" * 30)
    print(f"Type: {artist['type']}")
    print(f"URI: {artist['uri']}")

    # Get top tracks for more insights
    try:
        top_tracks = sp.artist_top_tracks(artist['id'])
        if top_tracks and 'tracks' in top_tracks:
            print(f"\n🎵 TOP TRACKS ({len(top_tracks['tracks'])} tracks)")
            print("-" * 30)
            for i, track in enumerate(top_tracks['tracks'][:5], 1):
                print(
                    f"{i}. {track['name']} (Popularity: {track['popularity']})")
    except Exception as e:
        print(f"Could not fetch top tracks: {e}")


# Get artist information with error handling
artist_id = "1uNFoZAHBGtllmzznpCI3s"  # Justin Bieber
artist = sp.artist(artist_id)

print_artist_details(artist)
