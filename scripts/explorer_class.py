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

    def explore_artists(self):
        """Explore Artists endpoint"""
        self.print_section_header("Artists", "🎤")

        # Get artist data
        artist = self.safe_api_call(self.sp.artist, self.sample_ids['artist'])
        if artist:
            self.print_fields(artist)
            self.print_sample_data(artist, 1000)

    def explore_albums(self):
        """Explore Albums endpoint"""
        pass

    def explore_genres(self):
        pass

    def explore_playlists(self):
        pass

    def explore_tracks(self):
        pass
