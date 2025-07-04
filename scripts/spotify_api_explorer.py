from explorer_class import SpotifyAPIExplorer


def main():
    """Main function"""
    try:
        explorer = SpotifyAPIExplorer()
        explorer.explore_all()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
