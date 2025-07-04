# Spotify Top Streamers Analytics

This project analyzes Spotify data to find the top 10 streamers of all time, regardless of country or music type.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pipenv install
```

### 2. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - App name: `Top Music Analytics`
   - App description: `Analytics for top streamers`
   - Redirect URI: `http://localhost:8888/callback`
5. Click "Save"
6. Copy your `Client ID` and `Client Secret`

### 3. Setup Environment Variables

Create a `.env` file in the project root:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### 4. Run the Analytics

```bash
# Basic artist info with detailed stats
pipenv run python spotify.py

# Top 10 streamers analysis
pipenv run python spotify_analytics.py

# Justin Bieber monthly listeners timeline
pipenv run python justin_bieber_timeline.py

# Kendrick Lamar vs Drake comparison (Jupyter Notebook)
pipenv run jupyter notebook kendrick_vs_drake_analysis.ipynb
```

## 📊 What the Scripts Do

### `spotify.py`

- Basic example showing how to get artist information
- Uses environment variables for security
- Includes error handling
- [API end points](https://developer.spotify.com/documentation/web-api)

### `spotify_analytics.py`

- Finds top 10 streamers globally
- Analyzes popularity, followers, and estimated streams
- Saves results to CSV file
- Provides detailed analytics output

### `justin_bieber_timeline.py`

- Tracks Justin Bieber's monthly listeners over his entire career
- Creates historical timeline with major career milestones
- Generates visualizations and CSV data
- Shows popularity and follower growth trends

### `kendrick_vs_drake_analysis.ipynb`

- Comprehensive Jupyter notebook comparing Kendrick Lamar vs Drake
- Analyzes streaming patterns over the last 5 years (2019-2024)
- Interactive visualizations and statistical analysis
- Determines winners in different categories
- Perfect for settling the "who's better" debate with data!

## 📁 Project Structure

```
topMusic/
├── .env                    # Your Spotify credentials (not in git)
├── .gitignore             # Excludes sensitive files
├── Pipfile                # Python dependencies
├── README.md              # This file
├── spotify.py                     # Basic Spotify API example
├── spotify_analytics.py           # Top streamers analysis
├── justin_bieber_timeline.py      # Justin Bieber career timeline
└── kendrick_vs_drake_analysis.ipynb  # Kendrick vs Drake comparison
```

## 🔒 Security Notes

- Never commit your `.env` file to git
- The `.gitignore` file excludes sensitive files
- Keep your Spotify credentials secure

## 📈 Understanding the Results

- **Popularity**: Spotify's popularity score (0-100)
- **Followers**: Number of Spotify followers
- **Estimated Streams**: Rough estimate based on track popularity
- **Genres**: Music genres the artist is associated with

## 🛠️ Troubleshooting

- **"Missing credentials"**: Check your `.env` file
- **Import errors**: Run `pipenv install` to install dependencies
- **API limits**: Spotify has rate limits, scripts include delays

## 📝 Notes

- Spotify doesn't provide exact streaming numbers publicly
- Estimates are based on popularity scores and track data
- Results may vary based on current trends and API data
