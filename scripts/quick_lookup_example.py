from scripts.spotify_id_collector import SpotifyIDCollector
import pandas as pd


def quick_lookup_demo():
    """Demonstrate quick ID lookups"""

    # Initialize the collector
    collector = SpotifyIDCollector()

    print("🔍 QUICK LOOKUP DEMO")
    print("=" * 40)

    # Try to load existing data first
    if not collector.load_lookup_dataframes():
        print("Creating new lookup data...")
        collector.create_lookup_dataframes()

    # Example 1: Look up artists by name
    print("\n🎤 ARTIST LOOKUPS:")
    print("-" * 20)

    artists_to_find = ["Drake", "Taylor Swift", "Kendrick Lamar", "Bad Bunny"]

    for artist_name in artists_to_find:
        artist_id = collector.lookup_artist_by_name(artist_name)
        if artist_id:
            print(f"✅ {artist_name}: {artist_id}")
        else:
            print(f"❌ {artist_name}: Not found")

    # Example 2: Look up tracks by name
    print("\n🎵 TRACK LOOKUPS:")
    print("-" * 20)

    tracks_to_find = ["God's Plan", "Blinding Lights",
                      "Shape of You", "Uptown Funk"]

    for track_name in tracks_to_find:
        track_id = collector.lookup_track_by_name(track_name)
        if track_id:
            print(f"✅ {track_name}: {track_id}")
        else:
            print(f"❌ {track_name}: Not found")

    # Example 3: Get detailed info using IDs
    print("\n📊 DETAILED INFO:")
    print("-" * 20)

    # Get Drake's info
    drake_id = collector.lookup_artist_by_name("Drake")
    if drake_id:
        drake_info = collector.get_artist_info(drake_id)
        if drake_info:
            print(f"🎤 {drake_info['name']}:")
            print(f"   • ID: {drake_info['id']}")
            print(f"   • Followers: {drake_info['followers']:,}")
            print(f"   • Popularity: {drake_info['popularity']}/100")
            print(f"   • Genres: {', '.join(drake_info['genres'][:3])}")

    # Get track info
    track_id = collector.lookup_track_by_name("God's Plan")
    if track_id:
        track_info = collector.get_track_info(track_id)
        if track_info:
            print(f"\n🎵 {track_info['name']}:")
            print(f"   • ID: {track_info['id']}")
            print(f"   • Artist: {track_info['artist']}")
            print(f"   • Album: {track_info['album']}")
            print(f"   • Popularity: {track_info['popularity']}/100")
            print(
                f"   • Duration: {track_info['duration_ms'] // 60000}:{(track_info['duration_ms'] % 60000) // 1000:02d}")

    # Example 4: Load and display the DataFrames
    print("\n📋 DATAFRAME PREVIEW:")
    print("-" * 20)

    # Load the CSV files
    artists_df = pd.read_csv('spotify_artists_lookup.csv')
    tracks_df = pd.read_csv('spotify_tracks_lookup.csv')

    print(f"\n🎤 Artists DataFrame ({len(artists_df)} rows):")
    print(artists_df[['name', 'spotify_id', 'popularity', 'followers']].head())

    print(f"\n🎵 Tracks DataFrame ({len(tracks_df)} rows):")
    print(tracks_df[['track_name', 'artist_name',
          'track_id', 'popularity']].head())

    # Example 5: Filter and search within DataFrames
    print("\n🔍 DATAFRAME FILTERING:")
    print("-" * 20)

    # Find all tracks by Drake
    drake_tracks = tracks_df[tracks_df['artist_name'].str.contains(
        'Drake', case=False, na=False)]
    if not drake_tracks.empty:
        print(f"\n🎵 Drake's tracks ({len(drake_tracks)} found):")
        for _, track in drake_tracks.head().iterrows():
            print(f"   • {track['track_name']} (ID: {track['track_id']})")

    # Find high-popularity tracks
    popular_tracks = tracks_df[tracks_df['popularity'] >= 80]
    print(f"\n🔥 High-popularity tracks ({len(popular_tracks)} found):")
    for _, track in popular_tracks.head().iterrows():
        print(
            f"   • {track['track_name']} by {track['artist_name']} (Popularity: {track['popularity']})")


def custom_search_example():
    """Example of custom searches"""

    collector = SpotifyIDCollector()

    print("\n🎯 CUSTOM SEARCH EXAMPLE")
    print("=" * 40)

    # Custom artist search
    custom_artists = ["The Beatles", "Queen",
                      "Michael Jackson", "Elvis Presley"]
    artists_df = collector.search_and_collect_artists(custom_artists, limit=2)

    print(f"\n✅ Found {len(artists_df)} artists:")
    for _, artist in artists_df.iterrows():
        print(f"   • {artist['name']} (ID: {artist['spotify_id']})")

    # Custom track search
    custom_tracks = ["Bohemian Rhapsody",
                     "Imagine", "Billie Jean", "Hound Dog"]
    tracks_df = collector.search_and_collect_tracks(custom_tracks, limit=2)

    print(f"\n✅ Found {len(tracks_df)} tracks:")
    for _, track in tracks_df.iterrows():
        print(
            f"   • {track['track_name']} by {track['artist_name']} (ID: {track['track_id']})")


if __name__ == "__main__":
    quick_lookup_demo()
    custom_search_example()
