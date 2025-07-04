import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import json
from datetime import datetime
import pandas as pd

# Load environment variables
load_dotenv()


def setup_spotify_client():
    """Setup Spotify client with credentials from environment variables"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("Missing Spotify credentials in .env file")

    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))


def explore_artist_data(sp, artist_id, artist_name):
    """Explore all available data for an artist"""
    print(f"🔍 EXPLORING SPOTIFY DATA FOR: {artist_name.upper()}")
    print("=" * 60)

    # 1. Basic Artist Information
    print("\n📋 1. BASIC ARTIST INFORMATION")
    print("-" * 30)
    try:
        artist = sp.artist(artist_id)
        print(f"Name: {artist['name']}")
        print(f"Spotify ID: {artist['id']}")
        print(f"Popularity Score: {artist['popularity']}/100")
        print(f"Followers: {artist['followers']['total']:,}")
        print(f"Genres: {', '.join(artist['genres'])}")
        print(f"Type: {artist['type']}")
        print(f"URI: {artist['uri']}")
        print(f"Spotify URL: {artist['external_urls']['spotify']}")
        if artist['images']:
            print(f"Profile Image: {artist['images'][0]['url']}")
    except Exception as e:
        print(f"Error getting artist info: {e}")

    # 2. Top Tracks
    print("\n🎵 2. TOP TRACKS (Last 4 weeks)")
    print("-" * 30)
    try:
        top_tracks = sp.artist_top_tracks(artist_id)
        if top_tracks and 'tracks' in top_tracks:
            for i, track in enumerate(top_tracks['tracks'][:5], 1):
                duration_min = track['duration_ms'] // 60000
                duration_sec = (track['duration_ms'] % 60000) // 1000
                print(f"{i}. {track['name']}")
                print(f"   Album: {track['album']['name']}")
                print(f"   Popularity: {track['popularity']}/100")
                print(f"   Duration: {duration_min}:{duration_sec:02d}")
                print(f"   Release Date: {track['album']['release_date']}")
                print(f"   Spotify URL: {track['external_urls']['spotify']}")
                print()
    except Exception as e:
        print(f"Error getting top tracks: {e}")

    # 3. Albums
    print("\n💿 3. ALBUMS")
    print("-" * 30)
    try:
        albums = sp.artist_albums(
            artist_id, album_type='album,single', limit=10)
        if albums and 'items' in albums:
            for i, album in enumerate(albums['items'][:5], 1):
                print(f"{i}. {album['name']}")
                print(f"   Type: {album['album_type']}")
                print(f"   Release Date: {album['release_date']}")
                print(f"   Total Tracks: {album['total_tracks']}")
                print(f"   Spotify URL: {album['external_urls']['spotify']}")
                print()
    except Exception as e:
        print(f"Error getting albums: {e}")

    # 4. Related Artists
    print("\n👥 4. RELATED ARTISTS")
    print("-" * 30)
    try:
        related = sp.artist_related_artists(artist_id)
        if related and 'artists' in related:
            for i, related_artist in enumerate(related['artists'][:5], 1):
                print(f"{i}. {related_artist['name']}")
                print(f"   Popularity: {related_artist['popularity']}/100")
                print(
                    f"   Followers: {related_artist['followers']['total']:,}")
                print(f"   Genres: {', '.join(related_artist['genres'][:3])}")
                print()
    except Exception as e:
        print(f"Error getting related artists: {e}")

    # 5. Audio Features for Top Tracks
    print("\n🎼 5. AUDIO FEATURES (for top tracks)")
    print("-" * 30)
    try:
        top_tracks = sp.artist_top_tracks(artist_id)
        if top_tracks and 'tracks' in top_tracks:
            track_ids = [track['id'] for track in top_tracks['tracks'][:3]]
            audio_features = sp.audio_features(track_ids)

            for i, features in enumerate(audio_features, 1):
                if features:
                    track_name = top_tracks['tracks'][i-1]['name']
                    print(f"{i}. {track_name}")
                    print(f"   Danceability: {features['danceability']:.2f}")
                    print(f"   Energy: {features['energy']:.2f}")
                    print(f"   Key: {features['key']}")
                    print(f"   Loudness: {features['loudness']:.2f} dB")
                    print(f"   Mode: {features['mode']}")
                    print(f"   Speechiness: {features['speechiness']:.2f}")
                    print(f"   Acousticness: {features['acousticness']:.2f}")
                    print(
                        f"   Instrumentalness: {features['instrumentalness']:.2f}")
                    print(f"   Liveness: {features['liveness']:.2f}")
                    print(f"   Valence: {features['valence']:.2f}")
                    print(f"   Tempo: {features['tempo']:.0f} BPM")
                    print()
    except Exception as e:
        print(f"Error getting audio features: {e}")

    # 6. Search for the artist (shows what's available in search)
    print("\n🔎 6. SEARCH RESULTS")
    print("-" * 30)
    try:
        search_results = sp.search(q=artist_name, type='artist', limit=5)
        if search_results and 'artists' in search_results:
            print(
                f"Found {search_results['artists']['total']} artists matching '{artist_name}'")
            for i, result in enumerate(search_results['artists']['items'][:3], 1):
                print(f"{i}. {result['name']}")
                print(f"   Popularity: {result['popularity']}/100")
                print(f"   Followers: {result['followers']['total']:,}")
                print(f"   Genres: {', '.join(result['genres'][:3])}")
                print()
    except Exception as e:
        print(f"Error searching: {e}")

    # 7. Available Markets
    print("\n🌍 7. AVAILABLE MARKETS")
    print("-" * 30)
    try:
        # Get markets from a track
        top_tracks = sp.artist_top_tracks(artist_id)
        if top_tracks and 'tracks' in top_tracks and top_tracks['tracks']:
            track = top_tracks['tracks'][0]
            print(
                f"Track '{track['name']}' available in {len(track['available_markets'])} markets")
            print(
                f"Sample markets: {', '.join(track['available_markets'][:10])}")
    except Exception as e:
        print(f"Error getting markets: {e}")


def show_api_limitations():
    """Show what data is NOT available from Spotify API"""
    print("\n🚫 SPOTIFY API LIMITATIONS")
    print("=" * 60)
    print("❌ Data NOT available from Spotify API:")
    print("   • Historical streaming numbers")
    print("   • Monthly listeners (exact numbers)")
    print("   • Daily/weekly streaming trends")
    print("   • Revenue data")
    print("   • Playlist performance metrics")
    print("   • User listening history")
    print("   • Geographic streaming breakdown")
    print("   • Time-based streaming patterns")
    print()
    print("✅ Data available from Spotify API:")
    print("   • Current popularity score (0-100)")
    print("   • Current follower count")
    print("   • Top tracks (last 4 weeks)")
    print("   • Album information")
    print("   • Audio features (danceability, energy, etc.)")
    print("   • Related artists")
    print("   • Genre information")
    print("   • Release dates")
    print("   • Available markets")
    print()
    print("💡 Alternative approaches for historical data:")
    print("   • Track popularity changes over time")
    print("   • Album release impact on popularity")
    print("   • Follower growth patterns")
    print("   • Audio feature evolution")
    print("   • Genre shifts over time")


def main():
    """Main function"""
    try:
        print("🎵 SPOTIFY DATA EXPLORER")
        print("=" * 60)

        # Setup client
        sp = setup_spotify_client()

        # Explore Drake's data
        DRAKE_ID = "3TVXtAsR1Inumwj472S9r4"
        explore_artist_data(sp, DRAKE_ID, "Drake")

        # Show API limitations
        show_api_limitations()

        print("\n💾 To save this data, you can:")
        print("   • Export to JSON/CSV")
        print("   • Store in database")
        print("   • Create visualizations")
        print("   • Track changes over time")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
