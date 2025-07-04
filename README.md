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

## API end points

[WebAPI](https://developer.spotify.com/documentation/web-api) and experminet using the [UI tool](https://developer.spotify.com/documentation/web-api/reference/get-an-album) to pull the right data in JSON.

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
