#!/usr/bin/env python3
"""
Script to fetch artist data from Spotify API using URIs from CSV

This script reads the artists_SpotifyID_with_uri.csv file and fetches detailed
artist information from Spotify API including name, followers, popularity,
images, href, and genres.
"""

import pandas as pd
import time
from setup.setupClient import setup_spotify_client
import os


def extract_artist_id_from_uri(uri):
    """
    Extract Spotify artist ID from a full Spotify URI
    Example: https://open.spotify.com/artist/3BJX1nYizKvWpZTY5HOAr4 -> 3BJX1nYizKvWpZTY5HOAr4
    """
    return uri.split('/')[-1]


def fetch_artist_data():
    """
    Read CSV with Spotify URIs and fetch artist data from Spotify API
    """
    # Define file paths
    input_file = "jupyter/artists_SpotifyID_with_uri.csv"
    output_file = "jupyter/artists_detailed_data.csv"

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Please run add_spotify_uri.py first to generate the CSV with URIs.")
        return

    try:
        # Setup Spotify client
        print("Setting up Spotify client...")
        sp = setup_spotify_client()

        # Read the CSV file
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        # Display basic info
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        # Initialize list to store artist data
        artist_data = []

        # Process artists with pagination and rate limiting
        total_artists = len(df)
        batch_size = 10  # Process 10 artists at a time
        total_batches = (total_artists + batch_size - 1) // batch_size

        print(f"\nFetching data for {total_artists} artists...")
        print(
            f"Processing in batches of {batch_size} artists ({total_batches} batches total)")
        print("Rate limiting: 1 second sleep after each batch of 10 requests")

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, total_artists)

            print(
                f"\n--- Batch {batch_num + 1}/{total_batches} (artists {start_idx + 1}-{end_idx}) ---")

            # Process current batch
            for idx in range(start_idx, end_idx):
                row = df.iloc[idx]
                try:
                    # Extract artist ID from URI
                    artist_id = extract_artist_id_from_uri(row['SpotifyURI'])

                    # Fetch artist data from Spotify API
                    artist_info = sp.artist(artist_id)

                    # Extract required information with proper null checks
                    if artist_info is None:
                        artist_info = {}

                    followers_data = artist_info.get('followers', {})
                    images_data = artist_info.get('images', [])

                    artist_entry = {
                        'name': artist_info.get('name', ''),
                        'followers': followers_data.get('total', 0) if followers_data else 0,
                        'popularity': artist_info.get('popularity', 0),
                        'image_url': images_data[0].get('url', '') if images_data else '',
                        'href': artist_info.get('href', ''),
                        # Join genres as comma-separated string
                        'genres': ','.join(artist_info.get('genres', []))
                    }

                    artist_data.append(artist_entry)
                    print(
                        f"  ✓ {idx + 1}/{total_artists}: {artist_entry['name']}")

                except Exception as e:
                    print(
                        f"  ✗ {idx + 1}/{total_artists}: Error processing {row.get('artistLabel', 'Unknown')}: {e}")
                    # Add empty entry for failed requests
                    artist_data.append({
                        'name': row.get('artistLabel', ''),
                        'followers': 0,
                        'popularity': 0,
                        'image_url': '',
                        'href': '',
                        'genres': ''
                    })

            # Rate limiting: 1 second sleep after each batch (except the last batch)
            if batch_num < total_batches - 1:
                print(f"  ⏳ Rate limiting: sleeping for 1 second...")
                time.sleep(1)

        # Create new DataFrame with fetched data
        print("\nCreating DataFrame with fetched data...")
        result_df = pd.DataFrame(artist_data)

        # Display sample of results
        print("\nSample of fetched data:")
        print(result_df.head())

        # Display summary statistics
        print(f"\nSummary:")
        print(f"  - Total artists processed: {len(result_df)}")
        print(
            f"  - Artists with followers > 0: {len(result_df[result_df['followers'] > 0])}")
        print(f"  - Average popularity: {result_df['popularity'].mean():.2f}")
        print(
            f"  - Artists with genres: {len(result_df[result_df['genres'] != ''])}")

        # Save the results
        print(f"\nSaving to {output_file}...")
        result_df.to_csv(output_file, index=False)

        print(f"Success! Artist data saved to {output_file}")

        return result_df

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    fetch_artist_data()
