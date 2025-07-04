import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import json
from datetime import datetime

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


def explore_albums(sp):
    """Explore Albums endpoint"""
    print("💿 ALBUMS ENDPOINT")
    print("=" * 50)

    try:
        # Get a popular album (Drake's "For All The Dogs")
        album_id = "2HpJwmx54r03VwyL7YMq9u"
        album = sp.album(album_id)

        print("Available fields:")
        for key in album.keys():
            print(f"   • {key}: {type(album[key]).__name__}")

        print("\nSample album data:")
        print(json.dumps(album, indent=2)[:1200] + "...")

        # Get album tracks
        tracks = sp.album_tracks(album_id)
        print(f"\nAlbum tracks structure (showing first track):")
        if tracks and 'items' in tracks and tracks['items']:
            track = tracks['items'][0]
            print("Track fields:")
            for key in track.keys():
                print(f"   • {key}: {type(track[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_artists(sp):
    """Explore Artists endpoint"""
    print("\n🎤 ARTISTS ENDPOINT")
    print("=" * 50)

    try:
        # Get Drake's artist info
        artist_id = "3TVXtAsR1Inumwj472S9r4"
        artist = sp.artist(artist_id)

        print("Available fields:")
        for key in artist.keys():
            print(f"   • {key}: {type(artist[key]).__name__}")

        print("\nSample artist data:")
        print(json.dumps(artist, indent=2)[:1000] + "...")

        # Get related artists
        related = sp.artist_related_artists(artist_id)
        print(f"\nRelated artists structure (showing first artist):")
        if related and 'artists' in related and related['artists']:
            related_artist = related['artists'][0]
            print("Related artist fields:")
            for key in related_artist.keys():
                print(f"   • {key}: {type(related_artist[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_audiobooks(sp):
    """Explore Audiobooks endpoint"""
    print("\n📚 AUDIOBOOKS ENDPOINT")
    print("=" * 50)

    try:
        # Search for audiobooks
        audiobooks = sp.search(q="Harry Potter", type="audiobook", limit=1)

        if audiobooks and 'audiobooks' in audiobooks and audiobooks['audiobooks']['items']:
            audiobook = audiobooks['audiobooks']['items'][0]

            print("Available fields:")
            for key in audiobook.keys():
                print(f"   • {key}: {type(audiobook[key]).__name__}")

            print("\nSample audiobook data:")
            print(json.dumps(audiobook, indent=2)[:800] + "...")
        else:
            print("No audiobooks found in search results")

    except Exception as e:
        print(f"Error: {e}")


def explore_categories(sp):
    """Explore Categories endpoint"""
    print("\n📂 CATEGORIES ENDPOINT")
    print("=" * 50)

    try:
        # Get categories
        categories = sp.categories()

        if categories and 'categories' in categories and categories['categories']['items']:
            category = categories['categories']['items'][0]

            print("Available fields:")
            for key in category.keys():
                print(f"   • {key}: {type(category[key]).__name__}")

            print("\nSample category data:")
            print(json.dumps(category, indent=2))

            # Get category playlists
            category_id = category['id']
            playlists = sp.category_playlists(category_id)
            print(f"\nCategory playlists structure (showing first playlist):")
            if playlists and 'playlists' in playlists and playlists['playlists']['items']:
                playlist = playlists['playlists']['items'][0]
                print("Playlist fields:")
                for key in playlist.keys():
                    print(f"   • {key}: {type(playlist[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_chapters(sp):
    """Explore Chapters endpoint"""
    print("\n📖 CHAPTERS ENDPOINT")
    print("=" * 50)

    try:
        # Search for shows to get chapter data
        shows = sp.search(q="podcast", type="show", limit=1)

        if shows and 'shows' in shows and shows['shows']['items']:
            show_id = shows['shows']['items'][0]['id']
            episodes = sp.show_episodes(show_id, limit=1)

            if episodes and 'items' in episodes and episodes['items']:
                episode_id = episodes['items'][0]['id']
                chapters = sp.episode_chapters(episode_id)

                if chapters and 'chapters' in chapters and chapters['chapters']['items']:
                    chapter = chapters['chapters']['items'][0]

                    print("Available fields:")
                    for key in chapter.keys():
                        print(f"   • {key}: {type(chapter[key]).__name__}")

                    print("\nSample chapter data:")
                    print(json.dumps(chapter, indent=2))
                else:
                    print("No chapters found for this episode")
            else:
                print("No episodes found for this show")
        else:
            print("No shows found in search results")

    except Exception as e:
        print(f"Error: {e}")


def explore_episodes(sp):
    """Explore Episodes endpoint"""
    print("\n🎧 EPISODES ENDPOINT")
    print("=" * 50)

    try:
        # Search for shows to get episode data
        shows = sp.search(q="podcast", type="show", limit=1)

        if shows and 'shows' in shows and shows['shows']['items']:
            show_id = shows['shows']['items'][0]['id']
            episodes = sp.show_episodes(show_id, limit=1)

            if episodes and 'items' in episodes and episodes['items']:
                episode = episodes['items'][0]

                print("Available fields:")
                for key in episode.keys():
                    print(f"   • {key}: {type(episode[key]).__name__}")

                print("\nSample episode data:")
                print(json.dumps(episode, indent=2)[:800] + "...")
            else:
                print("No episodes found for this show")
        else:
            print("No shows found in search results")

    except Exception as e:
        print(f"Error: {e}")


def explore_genres(sp):
    """Explore Genres endpoint"""
    print("\n🎼 GENRES ENDPOINT")
    print("=" * 50)

    try:
        # Get available genres
        genres = sp.recommendation_genres()

        if genres and 'genres' in genres:
            print("Available genres:")
            for i, genre in enumerate(genres['genres'][:10], 1):
                print(f"   {i}. {genre}")

            print(f"\nTotal genres available: {len(genres['genres'])}")
            print("\nSample genres data structure:")
            print(json.dumps(genres, indent=2))

    except Exception as e:
        print(f"Error: {e}")


def explore_markets(sp):
    """Explore Markets endpoint"""
    print("\n🌍 MARKETS ENDPOINT")
    print("=" * 50)

    try:
        # Get available markets
        markets = sp.available_markets()

        if markets and 'markets' in markets:
            print("Sample markets:")
            for i, market in enumerate(markets['markets'][:10], 1):
                print(f"   {i}. {market}")

            print(f"\nTotal markets available: {len(markets['markets'])}")
            print("\nSample markets data structure:")
            print(json.dumps(markets, indent=2))

    except Exception as e:
        print(f"Error: {e}")


def explore_player(sp):
    """Explore Player endpoint (requires user authentication)"""
    print("\n🎮 PLAYER ENDPOINT")
    print("=" * 50)
    print("⚠️  Player endpoints require user authentication (OAuth)")
    print("Available player endpoints:")
    print("   • sp.current_playback() - Get current playback")
    print("   • sp.currently_playing() - Get currently playing")
    print("   • sp.recently_played() - Get recently played")
    print("   • sp.devices() - Get available devices")
    print("   • sp.transfer_playback() - Transfer playback")
    print("   • sp.start_playback() - Start playback")
    print("   • sp.pause_playback() - Pause playback")
    print("   • sp.next_track() - Skip to next track")
    print("   • sp.previous_track() - Skip to previous track")
    print("   • sp.seek_track() - Seek to position")
    print("   • sp.repeat() - Set repeat mode")
    print("   • sp.shuffle() - Set shuffle mode")
    print("   • sp.volume() - Set volume")


def explore_playlists(sp):
    """Explore Playlists endpoint"""
    print("\n📜 PLAYLISTS ENDPOINT")
    print("=" * 50)

    try:
        # Get a popular playlist (Global Top 50)
        playlist_id = "37i9dQZEVXbMDoHDwVN2tF"
        playlist = sp.playlist(playlist_id)

        print("Available fields:")
        for key in playlist.keys():
            print(f"   • {key}: {type(playlist[key]).__name__}")

        print("\nSample playlist data:")
        print(json.dumps(playlist, indent=2)[:1000] + "...")

        # Get playlist tracks
        tracks = sp.playlist_tracks(playlist_id, limit=1)
        print(f"\nPlaylist tracks structure (showing first track):")
        if tracks and 'items' in tracks and tracks['items']:
            track_item = tracks['items'][0]
            print("Track item fields:")
            for key in track_item.keys():
                print(f"   • {key}: {type(track_item[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_search(sp):
    """Explore Search endpoint"""
    print("\n🔍 SEARCH ENDPOINT")
    print("=" * 50)

    try:
        # Search for different types
        search_types = ['artist', 'track', 'album',
                        'playlist', 'show', 'episode', 'audiobook']

        for search_type in search_types[:3]:  # Show first 3 types
            print(f"\nSearch type: {search_type}")
            results = sp.search(q="Drake", type=search_type, limit=1)

            if results and search_type + 's' in results and results[search_type + 's']['items']:
                item = results[search_type + 's']['items'][0]
                print("Available fields:")
                for key in item.keys():
                    print(f"   • {key}: {type(item[key]).__name__}")

                print("Sample data:")
                print(json.dumps(item, indent=2)[:600] + "...")

    except Exception as e:
        print(f"Error: {e}")


def explore_shows(sp):
    """Explore Shows endpoint"""
    print("\n🎙️ SHOWS ENDPOINT")
    print("=" * 50)

    try:
        # Search for shows
        shows = sp.search(q="podcast", type="show", limit=1)

        if shows and 'shows' in shows and shows['shows']['items']:
            show = shows['shows']['items'][0]

            print("Available fields:")
            for key in show.keys():
                print(f"   • {key}: {type(show[key]).__name__}")

            print("\nSample show data:")
            print(json.dumps(show, indent=2)[:800] + "...")

            # Get show episodes
            show_id = show['id']
            episodes = sp.show_episodes(show_id, limit=1)
            print(f"\nShow episodes structure (showing first episode):")
            if episodes and 'items' in episodes and episodes['items']:
                episode = episodes['items'][0]
                print("Episode fields:")
                for key in episode.keys():
                    print(f"   • {key}: {type(episode[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_tracks(sp):
    """Explore Tracks endpoint"""
    print("\n🎵 TRACKS ENDPOINT")
    print("=" * 50)

    try:
        # Get a popular track (Drake's "God's Plan")
        track_id = "6rqhFgbbKwnb9MLmUQDhG6"
        track = sp.track(track_id)

        print("Available fields:")
        for key in track.keys():
            print(f"   • {key}: {type(track[key]).__name__}")

        print("\nSample track data:")
        print(json.dumps(track, indent=2)[:1000] + "...")

        # Get audio features
        features = sp.audio_features([track_id])
        if features and features[0]:
            print(f"\nAudio features structure:")
            feature = features[0]
            print("Audio feature fields:")
            for key, value in feature.items():
                print(f"   • {key}: {value} ({type(value).__name__})")

        # Get audio analysis
        analysis = sp.audio_analysis(track_id)
        if analysis:
            print(f"\nAudio analysis structure (showing sections):")
            if 'sections' in analysis and analysis['sections']:
                section = analysis['sections'][0]
                print("Section fields:")
                for key in section.keys():
                    print(f"   • {key}: {type(section[key]).__name__}")

    except Exception as e:
        print(f"Error: {e}")


def explore_users(sp):
    """Explore Users endpoint (requires user authentication)"""
    print("\n👤 USERS ENDPOINT")
    print("=" * 50)
    print("⚠️  User endpoints require user authentication (OAuth)")
    print("Available user endpoints:")
    print("   • sp.current_user() - Get current user profile")
    print("   • sp.current_user_playlists() - Get user's playlists")
    print("   • sp.current_user_top_tracks() - Get user's top tracks")
    print("   • sp.current_user_top_artists() - Get user's top artists")
    print("   • sp.current_user_recently_played() - Get recently played")
    print("   • sp.current_user_saved_tracks() - Get saved tracks")
    print("   • sp.current_user_saved_albums() - Get saved albums")
    print("   • sp.current_user_saved_shows() - Get saved shows")
    print("   • sp.current_user_saved_episodes() - Get saved episodes")
    print("   • sp.user_playlists(user_id) - Get user's public playlists")
    print("   • sp.user_playlist(user_id, playlist_id) - Get specific playlist")


def main():
    """Main function to explore all endpoints"""
    try:
        print("🎵 SPOTIFY API COMPREHENSIVE EXPLORER")
        print("=" * 80)
        print(
            "This script explores all major Spotify API endpoints and their data structures")
        print("=" * 80)

        # Setup client
        sp = setup_spotify_client()

        # Explore all endpoints
        explore_albums(sp)
        explore_artists(sp)
        explore_audiobooks(sp)
        explore_categories(sp)
        explore_chapters(sp)
        explore_episodes(sp)
        explore_genres(sp)
        explore_markets(sp)
        explore_player(sp)
        explore_playlists(sp)
        explore_search(sp)
        explore_shows(sp)
        explore_tracks(sp)
        explore_users(sp)

        print("\n" + "=" * 80)
        print("✅ EXPLORATION COMPLETE!")
        print("=" * 80)
        print("Key insights:")
        print("   • Most endpoints return rich JSON data with metadata")
        print("   • User-related endpoints require OAuth authentication")
        print("   • Audio features provide detailed musical analysis")
        print("   • Search is available for all content types")
        print("   • Playlists and categories enable content discovery")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
