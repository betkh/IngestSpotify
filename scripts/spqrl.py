import csv
import requests
import time

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
LIMIT = 100
MAX_ROWS = 1000

all_results = []

for offset in range(0, MAX_ROWS, LIMIT):
    print(f"Fetching results {offset} to {offset + LIMIT}...")

    query = f"""
    SELECT ?artist ?artistLabel ?spotifyID WHERE {{
      ?artist wdt:P31 wd:Q5;
              wdt:P106 wd:Q639669;
              wdt:P1902 ?spotifyID.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {LIMIT}
    OFFSET {offset}
    """

    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "YourAppName/1.0 (your@email.com)"
    }

    response = requests.get(SPARQL_ENDPOINT, params={
                            "query": query}, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, stopping early.")
        break

    data = response.json()
    results = data["results"]["bindings"]

    if not results:
        print("No more data found.")
        break

    for r in results:
        artist_name = r["artistLabel"]["value"]
        artist_uri = r["artist"]["value"]
        spotify_id = r["spotifyID"]["value"]
        all_results.append({
            "name": artist_name,
            "wikidata_id": artist_uri.split("/")[-1],
            "spotify_id": spotify_id,
            "spotify_url": f"https://open.spotify.com/artist/{spotify_id}"
        })

    # Be nice to Wikidata – wait a bit
    time.sleep(1)

print(f"\n✅ Total records fetched: {len(all_results)}")

# Save to CSV
with open("spotify_artist_ids.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["name", "wikidata_id", "spotify_id", "spotify_url"])
    writer.writeheader()
    writer.writerows(all_results)

print("📁 Saved to: wikidata_ethiopian_artists_spotify.csv")
