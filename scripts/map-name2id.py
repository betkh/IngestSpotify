from setup.setupClient import setup_spotify_client

sp = setup_spotify_client()


artist_names = ["Drake", "Kendrick Lamar", "Eminem"]
spotify_ids = {}

artist_names = ["Drake", "Kendrick Lamar", "Eminem"]
artist_urls = {}

for name in artist_names:
    result = sp.search(q=name, type='artist', limit=1)

    print(result)
    break

    if result['artists']['items']:
        artist = result['artists']['items'][0]
        artist_id = artist['id']
        artist_url = f"https://open.spotify.com/artist/{artist_id}"
        artist_urls[name] = artist_url

print(artist_urls)
