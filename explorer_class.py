from dotenv import load_dotenv
import json
from typing import Dict, Any, Optional

from setup.setupClient import setup_spotify_client

# Load environment variables
load_dotenv()


class SpotifyAPIExplorer:
    """Comprehensive Spotify API Explorer using OOP design"""

    def __init__(self):
        """Initialize the explorer with Spotify client"""
        self.sp = setup_spotify_client()
        self.sample_ids = {
            'artist': "3TVXtAsR1Inumwj472S9r4",  # Drake
            'album': "2HpJwmx54r03VwyL7YMq9u",   # For All The Dogs
            'track': "6rqhFgbbKwnb9MLmUQDhG6",   # God's Plan
            'playlist': "37i9dQZEVXbMDoHDwVN2tF"  # Global Top 50
        }

    def print_section_header(self, title: str, emoji: str = "📋"):
        """Print a formatted section header"""
        print(f"\n{emoji} {title.upper()}")
        print("=" * 50)

    def print_fields(self, data: Dict[str, Any], title: str = "Available fields"):
        """Print available fields in a data structure"""
        print(f"{title}:")
        for key in data.keys():
            print(f"   • {key}: {type(data[key]).__name__}")

    def print_sample_data(self, data: Dict[str, Any], max_length: int = 1000):
        """Print sample JSON data"""
        print("\nSample data:")
        print(json.dumps(data, indent=2)[:max_length] + "...")

    def safe_api_call(self, func, *args, **kwargs) -> Optional[Any]:
        """Safely execute API calls with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def explore_albums(self):
        """Explore Albums endpoint"""
        self.print_section_header("Albums", "💿")

        # Get album data
        album = self.safe_api_call(self.sp.album, self.sample_ids['album'])
        if album:
            self.print_fields(album)
            self.print_sample_data(album, 1200)

            # Get album tracks
            tracks = self.safe_api_call(
                self.sp.album_tracks, self.sample_ids['album'])
            if tracks and 'items' in tracks and tracks['items']:
                track = tracks['items'][0]
                print(f"\nAlbum tracks structure (showing first track):")
                self.print_fields(track, "Track fields")

    def explore_artists(self):
        """Explore Artists endpoint"""
        self.print_section_header("Artists", "🎤")

        # Get artist data
        artist = self.safe_api_call(self.sp.artist, self.sample_ids['artist'])
        if artist:
            self.print_fields(artist)
            self.print_sample_data(artist, 1000)

            # Get related artists
            related = self.safe_api_call(
                self.sp.artist_related_artists, self.sample_ids['artist'])
            if related and 'artists' in related and related['artists']:
                related_artist = related['artists'][0]
                print(f"\nRelated artists structure (showing first artist):")
                self.print_fields(related_artist, "Related artist fields")

    def explore_audiobooks(self):
        """Explore Audiobooks endpoint"""
        self.print_section_header("Audiobooks", "📚")

        audiobooks = self.safe_api_call(
            self.sp.search, q="Harry Potter", type="audiobook", limit=1)
        if audiobooks and 'audiobooks' in audiobooks and audiobooks['audiobooks']['items']:
            audiobook = audiobooks['audiobooks']['items'][0]
            self.print_fields(audiobook)
            self.print_sample_data(audiobook, 800)
        else:
            print("No audiobooks found in search results")

    def explore_categories(self):
        """Explore Categories endpoint"""
        self.print_section_header("Categories", "📂")

        categories = self.safe_api_call(self.sp.categories)
        if categories and 'categories' in categories and categories['categories']['items']:
            category = categories['categories']['items'][0]
            self.print_fields(category)
            self.print_sample_data(category)

            # Get category playlists
            category_id = category['id']
            playlists = self.safe_api_call(
                self.sp.category_playlists, category_id)
            if playlists and 'playlists' in playlists and playlists['playlists']['items']:
                playlist = playlists['playlists']['items'][0]
                print(f"\nCategory playlists structure (showing first playlist):")
                self.print_fields(playlist, "Playlist fields")

    def explore_chapters(self):
        """Explore Chapters endpoint"""
        self.print_section_header("Chapters", "📖")

        # Get chapters through shows -> episodes -> chapters
        shows = self.safe_api_call(
            self.sp.search, q="podcast", type="show", limit=1)
        if shows and 'shows' in shows and shows['shows']['items']:
            show_id = shows['shows']['items'][0]['id']
            episodes = self.safe_api_call(
                self.sp.show_episodes, show_id, limit=1)

            if episodes and 'items' in episodes and episodes['items']:
                episode_id = episodes['items'][0]['id']
                # Note: episode_chapters might not be available in all spotipy versions
                try:
                    chapters = self.sp.episode_chapters(episode_id)
                except AttributeError:
                    print(
                        "episode_chapters method not available in this spotipy version")
                    chapters = None

                if chapters and 'chapters' in chapters and chapters['chapters']['items']:
                    chapter = chapters['chapters']['items'][0]
                    self.print_fields(chapter)
                    self.print_sample_data(chapter)
                else:
                    print("No chapters found for this episode")
            else:
                print("No episodes found for this show")
        else:
            print("No shows found in search results")

    def explore_episodes(self):
        """Explore Episodes endpoint"""
        self.print_section_header("Episodes", "🎧")

        shows = self.safe_api_call(
            self.sp.search, q="podcast", type="show", limit=1)
        if shows and 'shows' in shows and shows['shows']['items']:
            show_id = shows['shows']['items'][0]['id']
            episodes = self.safe_api_call(
                self.sp.show_episodes, show_id, limit=1)

            if episodes and 'items' in episodes and episodes['items']:
                episode = episodes['items'][0]
                self.print_fields(episode)
                self.print_sample_data(episode, 800)
            else:
                print("No episodes found for this show")
        else:
            print("No shows found in search results")

    def explore_genres(self):
        """Explore Genres endpoint"""
        self.print_section_header("Genres", "🎼")

        # Note: recommendation_genres might not be available in all spotipy versions
        try:
            genres = self.sp.recommendation_genres()
        except AttributeError:
            print("recommendation_genres method not available in this spotipy version")
            genres = None

        if genres and 'genres' in genres:
            print("Available genres:")
            for i, genre in enumerate(genres['genres'][:10], 1):
                print(f"   {i}. {genre}")

            print(f"\nTotal genres available: {len(genres['genres'])}")
            print("\nSample genres data structure:")
            print(json.dumps(genres, indent=2))

    def explore_markets(self):
        """Explore Markets endpoint"""
        self.print_section_header("Markets", "🌍")

        markets = self.safe_api_call(self.sp.available_markets)
        if markets and 'markets' in markets:
            print("Sample markets:")
            for i, market in enumerate(markets['markets'][:10], 1):
                print(f"   {i}. {market}")

            print(f"\nTotal markets available: {len(markets['markets'])}")
            print("\nSample markets data structure:")
            print(json.dumps(markets, indent=2))

    def explore_player(self):
        """Explore Player endpoint (requires user authentication)"""
        self.print_section_header("Player", "🎮")
        print("⚠️  Player endpoints require user authentication (OAuth)")
        print("Available player endpoints:")

        player_endpoints = [
            "sp.current_playback() - Get current playback",
            "sp.currently_playing() - Get currently playing",
            "sp.recently_played() - Get recently played",
            "sp.devices() - Get available devices",
            "sp.transfer_playback() - Transfer playback",
            "sp.start_playback() - Start playback",
            "sp.pause_playback() - Pause playback",
            "sp.next_track() - Skip to next track",
            "sp.previous_track() - Skip to previous track",
            "sp.seek_track() - Seek to position",
            "sp.repeat() - Set repeat mode",
            "sp.shuffle() - Set shuffle mode",
            "sp.volume() - Set volume"
        ]

        for endpoint in player_endpoints:
            print(f"   • {endpoint}")

    def explore_playlists(self):
        """Explore Playlists endpoint"""
        self.print_section_header("Playlists", "📜")

        playlist = self.safe_api_call(
            self.sp.playlist, self.sample_ids['playlist'])
        if playlist:
            self.print_fields(playlist)
            self.print_sample_data(playlist, 1000)

            # Get playlist tracks
            tracks = self.safe_api_call(
                self.sp.playlist_tracks, self.sample_ids['playlist'], limit=1)
            if tracks and 'items' in tracks and tracks['items']:
                track_item = tracks['items'][0]
                print(f"\nPlaylist tracks structure (showing first track):")
                self.print_fields(track_item, "Track item fields")

    def explore_search(self):
        """Explore Search endpoint"""
        self.print_section_header("Search", "🔍")

        search_types = ['artist', 'track', 'album',
                        'playlist', 'show', 'episode', 'audiobook']

        for search_type in search_types[:3]:  # Show first 3 types
            print(f"\nSearch type: {search_type}")
            results = self.safe_api_call(
                self.sp.search, q="Drake", type=search_type, limit=1)

            if results and search_type + 's' in results and results[search_type + 's']['items']:
                item = results[search_type + 's']['items'][0]
                self.print_fields(item)
                print("Sample data:")
                print(json.dumps(item, indent=2)[:600] + "...")

    def explore_shows(self):
        """Explore Shows endpoint"""
        self.print_section_header("Shows", "🎙️")

        shows = self.safe_api_call(
            self.sp.search, q="podcast", type="show", limit=1)
        if shows and 'shows' in shows and shows['shows']['items']:
            show = shows['shows']['items'][0]
            self.print_fields(show)
            self.print_sample_data(show, 800)

            # Get show episodes
            show_id = show['id']
            episodes = self.safe_api_call(
                self.sp.show_episodes, show_id, limit=1)
            if episodes and 'items' in episodes and episodes['items']:
                episode = episodes['items'][0]
                print(f"\nShow episodes structure (showing first episode):")
                self.print_fields(episode, "Episode fields")

    def explore_tracks(self):
        """Explore Tracks endpoint"""
        self.print_section_header("Tracks", "🎵")

        track = self.safe_api_call(self.sp.track, self.sample_ids['track'])
        if track:
            self.print_fields(track)
            self.print_sample_data(track, 1000)

            # Get audio features
            features = self.safe_api_call(self.sp.audio_features, [
                                          self.sample_ids['track']])
            if features and features[0]:
                print(f"\nAudio features structure:")
                feature = features[0]
                print("Audio feature fields:")
                for key, value in feature.items():
                    print(f"   • {key}: {value} ({type(value).__name__})")

            # Get audio analysis
            analysis = self.safe_api_call(
                self.sp.audio_analysis, self.sample_ids['track'])
            if analysis and 'sections' in analysis and analysis['sections']:
                section = analysis['sections'][0]
                print(f"\nAudio analysis structure (showing sections):")
                self.print_fields(section, "Section fields")

    def explore_users(self):
        """Explore Users endpoint (requires user authentication)"""
        self.print_section_header("Users", "👤")
        print("⚠️  User endpoints require user authentication (OAuth)")
        print("Available user endpoints:")

        user_endpoints = [
            "sp.current_user() - Get current user profile",
            "sp.current_user_playlists() - Get user's playlists",
            "sp.current_user_top_tracks() - Get user's top tracks",
            "sp.current_user_top_artists() - Get user's top artists",
            "sp.current_user_recently_played() - Get recently played",
            "sp.current_user_saved_tracks() - Get saved tracks",
            "sp.current_user_saved_albums() - Get saved albums",
            "sp.current_user_saved_shows() - Get saved shows",
            "sp.current_user_saved_episodes() - Get saved episodes",
            "sp.user_playlists(user_id) - Get user's public playlists",
            "sp.user_playlist(user_id, playlist_id) - Get specific playlist"
        ]

        for endpoint in user_endpoints:
            print(f"   • {endpoint}")

    def explore_all(self):
        """Explore all endpoints"""
        print("🎵 SPOTIFY API COMPREHENSIVE EXPLORER")
        print("=" * 80)
        print(
            "This script explores all major Spotify API endpoints and their data structures")
        print("=" * 80)

        # List of exploration methods
        exploration_methods = [
            self.explore_albums,
            self.explore_artists,
            self.explore_audiobooks,
            self.explore_categories,
            self.explore_chapters,
            self.explore_episodes,
            self.explore_genres,
            self.explore_markets,
            self.explore_player,
            self.explore_playlists,
            self.explore_search,
            self.explore_shows,
            self.explore_tracks,
            self.explore_users
        ]

        # Execute all exploration methods
        for method in exploration_methods:
            method()

        self.print_summary()

    def print_summary(self):
        """Print exploration summary"""
        print("\n" + "=" * 80)
        print("✅ EXPLORATION COMPLETE!")
        print("=" * 80)
        print("Key insights:")
        print("   • Most endpoints return rich JSON data with metadata")
        print("   • User-related endpoints require OAuth authentication")
        print("   • Audio features provide detailed musical analysis")
        print("   • Search is available for all content types")
        print("   • Playlists and categories enable content discovery")
        print("   • OOP design eliminates code redundancy")
        print("   • Error handling ensures robust exploration")
