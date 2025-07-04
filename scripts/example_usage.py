from explorer_class import SpotifyAPIExplorer


def example_usage():
    """Example usage of the SpotifyAPIExplorer class"""

    print("🎵 SPOTIFY API EXPLORER - EXAMPLE USAGE")
    print("=" * 50)

    # Create explorer instance
    explorer = SpotifyAPIExplorer()

    # Explore just artists
    explorer.explore_artists()


def main():
    """Main function"""
    try:
        example_usage()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
