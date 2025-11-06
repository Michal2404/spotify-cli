# 🎵 Spotify CLI

A powerful command-line interface for controlling Spotify from your terminal. Play music, manage playlists, search for tracks, and control playback - all without leaving the command line!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎮 **Playback Control** - Play, pause, skip tracks, and adjust volume
- 🔍 **Search** - Find tracks, artists, albums, and playlists
- 📚 **Playlist Management** - View and browse your playlists
- 🎯 **Current Track Info** - See what's playing right now
- 📱 **Device Management** - List and switch between Spotify devices
- 🌟 **Top Tracks** - View your most played tracks
- 🚀 **Fast & Lightweight** - No GUI required

## 📋 Prerequisites

- Python 3.7 or higher
- A Spotify account (Free or Premium)
- Spotify API credentials (free to obtain)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Michal2404/spotify-cli.git
cd spotify-cli
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install the package

```bash
pip install -e .
```

## 🔑 Setup Spotify API Credentials

### 1. Get your API credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create an App"**
4. Fill in the app name and description (e.g., "Spotify CLI")
5. Accept the terms and click **"Create"**
6. Click **"Settings"**
7. Copy your **Client ID** and **Client Secret**
8. Click **"Edit Settings"**
9. Add `http://localhost:8888/callback` to **Redirect URIs**
10. Click **"Save"**

### 2. Create configuration file

Create a file named `.spotify-cli.env` in your home directory:

```bash
nano ~/.spotify-cli.env
```

Add your credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

Save and close the file.

### 3. First run authentication

The first time you run the CLI, you'll be prompted to authorize the app:

```bash
spotify play --open
```

A browser window will open. Log in and authorize the app. You'll be redirected to a URL - copy and paste it back into the terminal when prompted.

## 📖 Usage

### Playback Control

```bash
# Show what's currently playing
spotify now

# Resume playback
spotify play

# Play a specific track (use Spotify URI)
spotify play spotify:track:3n3Ppam7vgaVa1iaRUc9Lp

# Open web player if no device is active
spotify play --open

# Pause playback
spotify pause

# Skip to next track
spotify next

# Go to previous track
spotify prev

# Set volume (0-100)
spotify volume 50
```

### Search

```bash
# Search for tracks (default)
spotify search "bohemian rhapsody"

# Search for artists
spotify search "queen" --type artist

# Search for albums
spotify search "a night at the opera" --type album

# Limit results
spotify search "love" --limit 5
```

### Playlists

```bash
# List your playlists
spotify playlists

# Show tracks in a playlist (use Spotify URI)
spotify playlist spotify:playlist:37i9dQZF1DXcBWIGoYBM5M

# Limit number of playlists shown
spotify playlists --limit 10
```

### Devices

```bash
# List available Spotify devices
spotify devices
```

### Statistics

```bash
# Show your top tracks (last 6 months)
spotify top

# Top tracks from last 4 weeks
spotify top --range short

# Top tracks of all time
spotify top --range long

# Show more results
spotify top --limit 20
```

## 🎯 Examples

```bash
# Morning routine: start playing your Discover Weekly
spotify search "discover weekly" --type playlist
spotify play spotify:playlist:37i9dQZEVXcQ9COmYvdajy

# Quick music control while coding
spotify pause
spotify next
spotify volume 30

# Discover new music
spotify top --range short --limit 5
spotify search "chill vibes" --type playlist
```

## 🛠️ Troubleshooting

### "No active device found" error

This means Spotify isn't running on any device. To fix:

1. Open Spotify on your computer, phone, or web browser
2. Start playing any track
3. Try your command again

Or use:
```bash
spotify play --open
```

This will automatically open Spotify Web Player for you.

### Authentication issues

If you're having trouble authenticating:

1. Delete the cache file: `rm ~/.spotify-cli-cache`
2. Check your credentials in `~/.spotify-cli.env`
3. Make sure the redirect URI in your Spotify app settings matches exactly: `http://localhost:8888/callback`
4. Try authenticating again

### Command not found

If `spotify` command is not found after installation:

```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall
pip install -e . --force-reinstall
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Spotipy](https://spotipy.readthedocs.io/) - A Python library for the Spotify Web API
- Inspired by the need for quick music control without leaving the terminal

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for command-line enthusiasts**