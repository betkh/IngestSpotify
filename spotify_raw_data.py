from dotenv import load_dotenv
import json

from setup.setupClient import setup_spotify_client

# Load environment variables
load_dotenv()


def show_raw_data_structure(sp, artist_id, artist_name):
    """Show the raw JSON data structure from Spotify API"""
    print(f"🔍 RAW SPOTIFY DATA STRUCTURE FOR: {artist_name}")
    print("=" * 60)

    # 1. Artist Data Structure
    print("\n📋 1. ARTIST DATA STRUCTURE")
    print("-" * 40)
    try:
        artist = sp.artist(artist_id)
        print("Available fields in artist data:")
        for key in artist.keys():
            print(f"   • {key}: {type(artist[key]).__name__}")
        print()
        print("Sample artist data (first few fields):")
        print(json.dumps(artist, indent=2)[:1000] + "...")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Top Tracks Data Structure
    print("\n🎵 2. TOP TRACKS DATA STRUCTURE")
    print("-" * 40)
    try:
        top_tracks = sp.artist_top_tracks(artist_id)
        if top_tracks and 'tracks' in top_tracks and top_tracks['tracks']:
            track = top_tracks['tracks'][0]
            print("Available fields in track data:")
            for key in track.keys():
                print(f"   • {key}: {type(track[key]).__name__}")
            print()
            print("Sample track data:")
            print(json.dumps(track, indent=2)[:800] + "...")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Audio Features Data Structure
    print("\n🎼 3. AUDIO FEATURES DATA STRUCTURE")
    print("-" * 40)
    try:
        top_tracks = sp.artist_top_tracks(artist_id)
        if top_tracks and 'tracks' in top_tracks and top_tracks['tracks']:
            track_id = top_tracks['tracks'][0]['id']
            audio_features = sp.audio_features([track_id])
            if audio_features and audio_features[0]:
                features = audio_features[0]
                print("Available audio features:")
                for key, value in features.items():
                    print(f"   • {key}: {value} ({type(value).__name__})")
                print()
                print("Sample audio features data:")
                print(json.dumps(features, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    # 4. Album Data Structure
    print("\n💿 4. ALBUM DATA STRUCTURE")
    print("-" * 40)
    try:
        albums = sp.artist_albums(artist_id, album_type='album', limit=1)
        if albums and 'items' in albums and albums['items']:
            album = albums['items'][0]
            print("Available fields in album data:")
            for key in album.keys():
                print(f"   • {key}: {type(album[key]).__name__}")
            print()
            print("Sample album data:")
            print(json.dumps(album, indent=2)[:600] + "...")
    except Exception as e:
        print(f"Error: {e}")


def show_api_endpoints():
    """Show available Spotify API endpoints"""
    print("\n🔗 AVAILABLE SPOTIFY API ENDPOINTS")
    print("=" * 60)
    print("Artist-related endpoints:")
    print("   • sp.artist(artist_id) - Get artist info")
    print("   • sp.artist_top_tracks(artist_id) - Get top tracks")
    print("   • sp.artist_albums(artist_id) - Get albums")
    print("   • sp.artist_related_artists(artist_id) - Get related artists")
    print()
    print("Track-related endpoints:")
    print("   • sp.track(track_id) - Get track info")
    print("   • sp.audio_features(track_ids) - Get audio features")
    print("   • sp.audio_analysis(track_id) - Get detailed audio analysis")
    print()
    print("Search endpoints:")
    print("   • sp.search(q, type) - Search for artists/tracks/albums")
    print("   • sp.search(q, type, market) - Search in specific market")
    print()
    print("Playlist endpoints:")
    print("   • sp.playlist(playlist_id) - Get playlist info")
    print("   • sp.playlist_tracks(playlist_id) - Get playlist tracks")
    print()
    print("User endpoints (requires user authentication):")
    print("   • sp.current_user_playlists() - Get user's playlists")
    print("   • sp.current_user_top_tracks() - Get user's top tracks")
    print("   • sp.current_user_top_artists() - Get user's top artists")


def main():
    """Main function"""
    try:
        print("🎵 SPOTIFY RAW DATA EXPLORER")
        print("=" * 60)

        # Setup client
        sp = setup_spotify_client()

        # Show raw data structure for Drake
        DRAKE_ID = "3TVXtAsR1Inumwj472S9r4"
        show_raw_data_structure(sp, DRAKE_ID, "Drake")

        # Show available endpoints
        show_api_endpoints()

        print("\n💡 Key Insights:")
        print("   • Spotify API provides rich metadata but no streaming numbers")
        print("   • Popularity scores are relative (0-100)")
        print("   • Audio features provide detailed musical analysis")
        print("   • Release dates help track career progression")
        print("   • Follower counts show current audience size")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
