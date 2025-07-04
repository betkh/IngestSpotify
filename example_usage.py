from explorer_class import SpotifyAPIExplorer


def example_usage():
    """Example usage of the SpotifyAPIExplorer class"""

    print("🎵 SPOTIFY API EXPLORER - EXAMPLE USAGE")
    print("=" * 50)

    # Create explorer instance
    explorer = SpotifyAPIExplorer()

    # Example 1: Explore specific endpoints
    print("\n📋 Example 1: Explore specific endpoints")
    print("-" * 40)

    # Explore just artists
    explorer.explore_artists()

    # Explore just tracks
    explorer.explore_tracks()

    # Example 2: Custom exploration
    print("\n📋 Example 2: Custom exploration")
    print("-" * 40)

    # Get artist data directly
    artist = explorer.safe_api_call(
        explorer.sp.artist, explorer.sample_ids['artist'])
    if artist:
        print(f"Artist: {artist['name']}")
        print(f"Popularity: {artist['popularity']}/100")
        print(f"Followers: {artist['followers']['total']:,}")
        print(f"Genres: {', '.join(artist['genres'])}")

    # Example 3: Batch exploration
    print("\n📋 Example 3: Batch exploration")
    print("-" * 40)

    # Explore multiple endpoints in sequence
    endpoints_to_explore = [
        explorer.explore_albums,
        explorer.explore_playlists,
        explorer.explore_search
    ]

    for endpoint in endpoints_to_explore:
        endpoint()
        print("\n" + "="*30 + "\n")

    # Example 4: Data extraction
    print("\n📋 Example 4: Data extraction")
    print("-" * 40)

    # Extract track data
    track = explorer.safe_api_call(
        explorer.sp.track, explorer.sample_ids['track'])
    if track:
        track_data = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'spotify_url': track['external_urls']['spotify']
        }

        print("Extracted track data:")
        for key, value in track_data.items():
            print(f"  {key}: {value}")

    print("\n✅ Example usage complete!")


def main():
    """Main function"""
    try:
        example_usage()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
