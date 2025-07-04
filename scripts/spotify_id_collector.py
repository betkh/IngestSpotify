from dotenv import load_dotenv
import pandas as pd
import json
from typing import Dict, List, Any, Optional
import time

from setup.setupClient import setup_spotify_client

# Load environment variables
load_dotenv()


class SpotifyIDCollector:
    """Collect Spotify IDs for tracks and artists programmatically"""

    def __init__(self):
        """Initialize the collector with Spotify client"""
        self.sp = setup_spotify_client()
        self.artists_df = pd.DataFrame()
        self.tracks_df = pd.DataFrame()
        self.albums_df = pd.DataFrame()

    def safe_api_call(self, func, *args, **kwargs) -> Optional[Any]:
        """Safely execute API calls with error handling and rate limiting"""
        try:
            result = func(*args, **kwargs)
            time.sleep(0.1)  # Rate limiting to avoid hitting API limits
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    def search_and_collect_artists(self, search_terms: List[str], limit: int = 5) -> pd.DataFrame:
        """Search for artists and collect their IDs"""
        print(f"🔍 Searching for {len(search_terms)} artists...")

        artists_data = []

        for term in search_terms:
            print(f"Searching for: {term}")

            # Search for artists
            results = self.safe_api_call(
                self.sp.search, q=term, type='artist', limit=limit)

            if results and 'artists' in results and results['artists']['items']:
                for artist in results['artists']['items']:
                    artist_data = {
                        'search_term': term,
                        'spotify_id': artist['id'],
                        'name': artist['name'],
                        'popularity': artist['popularity'],
                        'followers': artist['followers']['total'],
                        # Top 3 genres
                        'genres': ', '.join(artist['genres'][:3]),
                        'spotify_url': artist['external_urls']['spotify'],
                        'image_url': artist['images'][0]['url'] if artist['images'] else None
                    }
                    artists_data.append(artist_data)

        self.artists_df = pd.DataFrame(artists_data)
        print(f"✅ Collected {len(self.artists_df)} artists")
        return self.artists_df

    def search_and_collect_tracks(self, search_terms: List[str], limit: int = 5) -> pd.DataFrame:
        """Search for tracks and collect their IDs"""
        print(f"🎵 Searching for {len(search_terms)} tracks...")

        tracks_data = []

        for term in search_terms:
            print(f"Searching for: {term}")

            # Search for tracks
            results = self.safe_api_call(
                self.sp.search, q=term, type='track', limit=limit)

            if results and 'tracks' in results and results['tracks']['items']:
                for track in results['tracks']['items']:
                    # Get duration in minutes and seconds
                    duration_ms = track['duration_ms']
                    duration_min = duration_ms // 60000
                    duration_sec = (duration_ms % 60000) // 1000

                    track_data = {
                        'search_term': term,
                        'spotify_id': track['id'],
                        'name': track['name'],
                        'artist_name': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                        'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                        'album_name': track['album']['name'],
                        'album_id': track['album']['id'],
                        'popularity': track['popularity'],
                        'duration_ms': duration_ms,
                        'duration_formatted': f"{duration_min}:{duration_sec:02d}",
                        'release_date': track['album']['release_date'],
                        'spotify_url': track['external_urls']['spotify'],
                        'preview_url': track['preview_url']
                    }
                    tracks_data.append(track_data)

        self.tracks_df = pd.DataFrame(tracks_data)
        print(f"✅ Collected {len(self.tracks_df)} tracks")
        return self.tracks_df

    def get_artist_top_tracks(self, artist_ids: List[str]) -> pd.DataFrame:
        """Get top tracks for specific artists"""
        print(f"🎤 Getting top tracks for {len(artist_ids)} artists...")

        top_tracks_data = []

        for artist_id in artist_ids:
            # Get artist info first
            artist = self.safe_api_call(self.sp.artist, artist_id)
            if not artist:
                continue

            print(f"Getting top tracks for: {artist['name']}")

            # Get top tracks
            top_tracks = self.safe_api_call(
                self.sp.artist_top_tracks, artist_id)

            if top_tracks and 'tracks' in top_tracks:
                for track in top_tracks['tracks']:
                    duration_ms = track['duration_ms']
                    duration_min = duration_ms // 60000
                    duration_sec = (duration_ms % 60000) // 1000

                    track_data = {
                        'artist_id': artist_id,
                        'artist_name': artist['name'],
                        'track_id': track['id'],
                        'track_name': track['name'],
                        'album_name': track['album']['name'],
                        'album_id': track['album']['id'],
                        'popularity': track['popularity'],
                        'duration_ms': duration_ms,
                        'duration_formatted': f"{duration_min}:{duration_sec:02d}",
                        'release_date': track['album']['release_date'],
                        'spotify_url': track['external_urls']['spotify']
                    }
                    top_tracks_data.append(track_data)

        top_tracks_df = pd.DataFrame(top_tracks_data)
        print(f"✅ Collected {len(top_tracks_df)} top tracks")
        return top_tracks_df

    def get_playlist_tracks(self, playlist_ids: List[str]) -> pd.DataFrame:
        """Get tracks from specific playlists"""
        print(f"📜 Getting tracks from {len(playlist_ids)} playlists...")

        playlist_tracks_data = []

        for playlist_id in playlist_ids:
            # Get playlist info first
            playlist = self.safe_api_call(self.sp.playlist, playlist_id)
            if not playlist:
                continue

            print(f"Getting tracks from: {playlist['name']}")

            # Get playlist tracks
            tracks = self.safe_api_call(self.sp.playlist_tracks, playlist_id)

            if tracks and 'items' in tracks:
                for item in tracks['items']:
                    if item and 'track' in item and item['track']:
                        track = item['track']

                        duration_ms = track['duration_ms']
                        duration_min = duration_ms // 60000
                        duration_sec = (duration_ms % 60000) // 1000

                        track_data = {
                            'playlist_id': playlist_id,
                            'playlist_name': playlist['name'],
                            'track_id': track['id'],
                            'track_name': track['name'],
                            'artist_name': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                            'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                            'album_name': track['album']['name'],
                            'album_id': track['album']['id'],
                            'popularity': track['popularity'],
                            'duration_ms': duration_ms,
                            'duration_formatted': f"{duration_min}:{duration_sec:02d}",
                            'release_date': track['album']['release_date'],
                            'spotify_url': track['external_urls']['spotify']
                        }
                        playlist_tracks_data.append(track_data)

        playlist_tracks_df = pd.DataFrame(playlist_tracks_data)
        print(f"✅ Collected {len(playlist_tracks_df)} playlist tracks")
        return playlist_tracks_df

    def create_lookup_dataframes(self):
        """Create comprehensive lookup DataFrames"""
        print("📊 Creating lookup DataFrames...")

        # Popular artists to search for
        popular_artists = [
            "Drake", "Kendrick Lamar", "Taylor Swift", "Ed Sheeran", "Ariana Grande",
            "Post Malone", "Billie Eilish", "The Weeknd", "Dua Lipa", "Bad Bunny",
            "Justin Bieber", "Beyoncé", "Rihanna", "Eminem", "Bruno Mars"
        ]

        # Popular tracks to search for
        popular_tracks = [
            "God's Plan", "Blinding Lights", "Shape of You", "Uptown Funk", "Despacito",
            "See You Again", "Thinking Out Loud", "Blank Space", "Roar", "Happy",
            "Dark Horse", "All of Me", "Counting Stars", "Stay With Me", "Shake It Off"
        ]

        # Popular playlists to extract tracks from
        popular_playlists = [
            "37i9dQZEVXbMDoHDwVN2tF",  # Global Top 50
            "37i9dQZF1DXcBWIGoYBM5M",  # Today's Top Hits
            "37i9dQZF1DX5Ejj0EkURtP",  # All Out 2010s
            "37i9dQZF1DX4sWSpwq3LiO",  # Peaceful Piano
            "37i9dQZF1DX0XUsuxWHRQd"   # RapCaviar
        ]

        # Collect data
        artists_df = self.search_and_collect_artists(popular_artists, limit=3)
        tracks_df = self.search_and_collect_tracks(popular_tracks, limit=3)

        # Get top tracks for collected artists
        artist_ids = artists_df['spotify_id'].tolist()
        top_tracks_df = self.get_artist_top_tracks(artist_ids)

        # Get tracks from popular playlists
        playlist_tracks_df = self.get_playlist_tracks(popular_playlists)

        # Combine all track data
        all_tracks_df = pd.concat(
            [tracks_df, top_tracks_df, playlist_tracks_df], ignore_index=True)

        # Remove duplicates based on track_id
        all_tracks_df = all_tracks_df.drop_duplicates(subset=['track_id'])

        # Save to CSV files
        artists_df.to_csv('spotify_artists_lookup.csv', index=False)
        all_tracks_df.to_csv('spotify_tracks_lookup.csv', index=False)

        print(f"\n💾 Saved lookup files:")
        print(f"   • spotify_artists_lookup.csv ({len(artists_df)} artists)")
        print(f"   • spotify_tracks_lookup.csv ({len(all_tracks_df)} tracks)")

        return artists_df, all_tracks_df

    def load_lookup_dataframes(self):
        """Load existing lookup DataFrames"""
        try:
            self.artists_df = pd.read_csv('spotify_artists_lookup.csv')
            self.tracks_df = pd.read_csv('spotify_tracks_lookup.csv')
            print(f"✅ Loaded existing lookup data:")
            print(f"   • {len(self.artists_df)} artists")
            print(f"   • {len(self.tracks_df)} tracks")
            return True
        except FileNotFoundError:
            print("❌ Lookup files not found. Run create_lookup_dataframes() first.")
            return False

    def lookup_artist_by_name(self, artist_name: str) -> Optional[str]:
        """Look up artist ID by name"""
        if self.artists_df.empty:
            if not self.load_lookup_dataframes():
                return None

        # Case-insensitive search
        matches = self.artists_df[self.artists_df['name'].str.lower(
        ).str.contains(artist_name.lower())]

        if not matches.empty:
            return matches.iloc[0]['spotify_id']
        return None

    def lookup_track_by_name(self, track_name: str) -> Optional[str]:
        """Look up track ID by name"""
        if self.tracks_df.empty:
            if not self.load_lookup_dataframes():
                return None

        # Case-insensitive search
        matches = self.tracks_df[self.tracks_df['track_name'].str.lower(
        ).str.contains(track_name.lower())]

        if not matches.empty:
            return matches.iloc[0]['track_id']
        return None

    def get_artist_info(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed artist information"""
        artist = self.safe_api_call(self.sp.artist, artist_id)
        if artist:
            return {
                'id': artist['id'],
                'name': artist['name'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'genres': artist['genres'],
                'spotify_url': artist['external_urls']['spotify']
            }
        return None

    def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed track information"""
        track = self.safe_api_call(self.sp.track, track_id)
        if track:
            return {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'spotify_url': track['external_urls']['spotify']
            }
        return None


def main():
    """Main function to demonstrate ID collection"""
    try:
        collector = SpotifyIDCollector()

        print("🎵 SPOTIFY ID COLLECTOR")
        print("=" * 50)

        # Create lookup DataFrames
        artists_df, tracks_df = collector.create_lookup_dataframes()

        print("\n📋 SAMPLE DATA:")
        print("-" * 30)

        # Show sample artists
        print("\n🎤 Sample Artists:")
        print(artists_df[['name', 'spotify_id',
              'popularity', 'followers']].head())

        # Show sample tracks
        print("\n🎵 Sample Tracks:")
        print(tracks_df[['track_name', 'artist_name',
              'track_id', 'popularity']].head())

        # Demonstrate lookup functionality
        print("\n🔍 LOOKUP EXAMPLES:")
        print("-" * 30)

        # Look up Drake
        drake_id = collector.lookup_artist_by_name("Drake")
        if drake_id:
            print(f"Drake ID: {drake_id}")
            drake_info = collector.get_artist_info(drake_id)
            if drake_info:
                print(
                    f"Drake Info: {drake_info['name']} - {drake_info['followers']:,} followers")

        # Look up a track
        track_id = collector.lookup_track_by_name("God's Plan")
        if track_id:
            print(f"God's Plan ID: {track_id}")
            track_info = collector.get_track_info(track_id)
            if track_info:
                print(
                    f"Track Info: {track_info['name']} by {track_info['artist']}")

        print("\n✅ ID collection complete! Use the CSV files for lookups.")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
