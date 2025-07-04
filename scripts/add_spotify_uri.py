#!/usr/bin/env python3
"""
Script to add Spotify URI column to artists_SpotifyID.csv

This script reads the artists_SpotifyID.csv file and adds a new column called 'SpotifyURI'
by combining the base Spotify artist URL with the spotifyID from each row.
"""

import pandas as pd
import os


def add_spotify_uri():
    """
    Read the artists_SpotifyID.csv file and add a SpotifyURI column.
    """
    # Define file paths
    input_file = "resources/artists_SpotifyID.csv"
    output_file = "jupyter/artists_SpotifyID_with_uri.csv"

    # Base Spotify artist URL
    spotify_base_url = "https://open.spotify.com/artist/"

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    try:
        # Read the CSV file
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        # Display basic info about the dataframe
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"First few rows:")
        print(df.head())

        # Add the SpotifyURI column
        print("\nAdding SpotifyURI column...")
        df['SpotifyURI'] = spotify_base_url + df['spotifyID']

        # Display a few examples of the new URIs
        print("\nExamples of generated Spotify URIs:")
        for i, row in df.head(5).iterrows():
            print(f"  {row['artistLabel']}: {row['SpotifyURI']}")

        # Save the updated dataframe
        print(f"\nSaving to {output_file}...")
        df.to_csv(output_file, index=False)

        print(f"Success! Updated CSV saved to {output_file}")
        print(f"Total rows processed: {len(df)}")

        # Display summary statistics
        print(f"\nSummary:")
        print(f"  - Original columns: {list(df.columns[:-1])}")
        print(f"  - New column added: SpotifyURI")
        print(f"  - Total columns: {len(df.columns)}")

    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    add_spotify_uri()
