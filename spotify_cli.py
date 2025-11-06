#!/usr/bin/env python3
"""
Spotify CLI - A command-line interface for Spotify
Requires: pip install spotipy python-dotenv
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import sys
import argparse
import webbrowser
from typing import Optional

# Load environment variables
# Try to load from current directory first, then from home directory
if os.path.exists('.env'):
    load_dotenv()
else:
    load_dotenv(os.path.join(os.path.expanduser('~'), '.spotify-cli.env'))

class SpotifyCLI:
    def __init__(self):
        """Initialize Spotify client with OAuth authentication"""
        # Store cache in home directory so it works from anywhere
        cache_path = os.path.join(os.path.expanduser('~'), '.spotify-cli-cache')
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback'),
            scope='user-read-playback-state user-modify-playback-state user-read-currently-playing '
                  'playlist-read-private playlist-modify-private playlist-modify-public '
                  'user-library-read user-library-modify user-top-read',
            cache_path=cache_path
        ))

    def check_active_device(self, auto_open: bool = False) -> bool:
        """Check if there's an active device, offer to open web player if not"""
        devices = self.sp.devices()
        
        if not devices['devices']:
            print("❌ No Spotify devices found!")
            print("\n💡 To use Spotify CLI, you need to:")
            print("   1. Open Spotify Desktop App, or")
            print("   2. Open Spotify on your phone, or")
            print("   3. Open Spotify Web Player")
            
            if auto_open:
                response = input("\n🌐 Would you like to open Spotify Web Player? (y/n): ")
                if response.lower() in ['y', 'yes']:
                    webbrowser.open('https://open.spotify.com')
                    print("\n✅ Web player opened! Wait a moment for it to load, then try your command again.")
            else:
                print("\n💡 Tip: Use 'spotify play --open' to automatically open web player")
            return False
        
        # Check if any device is active
        active_devices = [d for d in devices['devices'] if d['is_active']]
        
        if not active_devices:
            print("⚠️  Spotify devices found but none are active:")
            for device in devices['devices']:
                print(f"   • {device['name']} ({device['type']})")
            print("\n💡 Open Spotify on one of these devices and start playing something first.")
            return False
        
        return True

    def current_playback(self):
        """Display current playback information"""
        current = self.sp.current_playback()
        if not current or not current.get('item'):
            print("❌ Nothing is currently playing")
            return

        track = current['item']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        progress = current['progress_ms'] // 1000
        duration = track['duration_ms'] // 1000
        is_playing = current['is_playing']
        
        print(f"\n🎵 Now {'Playing' if is_playing else 'Paused'}:")
        print(f"   Track: {track['name']}")
        print(f"   Artist: {artists}")
        print(f"   Album: {track['album']['name']}")
        print(f"   Progress: {progress//60}:{progress%60:02d} / {duration//60}:{duration%60:02d}")
        if current.get('device'):
            print(f"   Device: {current['device']['name']}")

    def play(self, uri: Optional[str] = None, auto_open: bool = False):
        """Resume playback or play specific URI"""
        if not self.check_active_device(auto_open):
            return
            
        try:
            if uri:
                self.sp.start_playback(uris=[uri])
                print("▶️  Playing track")
            else:
                self.sp.start_playback()
                print("▶️  Playback resumed")
        except Exception as e:
            print(f"❌ Error: {e}")

    def pause(self):
        """Pause playback"""
        try:
            self.sp.pause_playback()
            print("⏸️  Playback paused")
        except Exception as e:
            print(f"❌ Error: {e}")

    def next_track(self):
        """Skip to next track"""
        try:
            self.sp.next_track()
            print("⏭️  Skipped to next track")
        except Exception as e:
            print(f"❌ Error: {e}")

    def previous_track(self):
        """Go to previous track"""
        try:
            self.sp.previous_track()
            print("⏮️  Back to previous track")
        except Exception as e:
            print(f"❌ Error: {e}")

    def search(self, query: str, type: str = 'track', limit: int = 10):
        """Search for tracks, artists, albums, or playlists"""
        results = self.sp.search(q=query, type=type, limit=limit)
        
        if type == 'track':
            tracks = results['tracks']['items']
            if not tracks:
                print("❌ No tracks found")
                return
            
            print(f"\n🔍 Search results for '{query}':\n")
            for i, track in enumerate(tracks, 1):
                artists = ', '.join([artist['name'] for artist in track['artists']])
                print(f"{i}. {track['name']} - {artists}")
                print(f"   URI: {track['uri']}\n")
        
        elif type == 'artist':
            artists = results['artists']['items']
            if not artists:
                print("❌ No artists found")
                return
            
            print(f"\n🔍 Artist results for '{query}':\n")
            for i, artist in enumerate(artists, 1):
                print(f"{i}. {artist['name']}")
                print(f"   Followers: {artist['followers']['total']:,}")
                print(f"   URI: {artist['uri']}\n")

        elif type == 'album':
            albums = results['albums']['items']
            if not albums:
                print("❌ No albums found")
                return
            
            print(f"\n🔍 Album results for '{query}':\n")
            for i, album in enumerate(albums, 1):
                artists = ', '.join([artist['name'] for artist in album['artists']])
                print(f"{i}. {album['name']} - {artists}")
                print(f"   Release: {album['release_date']}")
                print(f"   URI: {album['uri']}\n")

    def my_playlists(self, limit: int = 20):
        """List user's playlists"""
        playlists = self.sp.current_user_playlists(limit=limit)
        
        print("\n📚 Your Playlists:\n")
        for i, playlist in enumerate(playlists['items'], 1):
            print(f"{i}. {playlist['name']}")
            print(f"   Tracks: {playlist['tracks']['total']}")
            print(f"   URI: {playlist['uri']}\n")

    def playlist_tracks(self, playlist_uri: str):
        """Show tracks in a playlist"""
        playlist = self.sp.playlist(playlist_uri)
        
        print(f"\n📚 {playlist['name']}\n")
        for i, item in enumerate(playlist['tracks']['items'], 1):
            track = item['track']
            if track:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                print(f"{i}. {track['name']} - {artists}")

    def volume(self, level: int):
        """Set volume (0-100)"""
        try:
            level = max(0, min(100, level))
            self.sp.volume(level)
            print(f"🔊 Volume set to {level}%")
        except Exception as e:
            print(f"❌ Error: {e}")

    def devices(self):
        """List available devices"""
        devices = self.sp.devices()
        
        if not devices['devices']:
            print("❌ No devices found")
            return
        
        print("\n📱 Available Devices:\n")
        for device in devices['devices']:
            active = "✓" if device['is_active'] else " "
            print(f"[{active}] {device['name']} ({device['type']})")
            print(f"    ID: {device['id']}\n")

    def top_tracks(self, limit: int = 10, time_range: str = 'medium_term'):
        """Show user's top tracks"""
        results = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
        
        range_names = {
            'short_term': 'Last 4 Weeks',
            'medium_term': 'Last 6 Months',
            'long_term': 'All Time'
        }
        
        print(f"\n🌟 Your Top Tracks ({range_names.get(time_range, time_range)}):\n")
        for i, track in enumerate(results['items'], 1):
            artists = ', '.join([artist['name'] for artist in track['artists']])
            print(f"{i}. {track['name']} - {artists}")


def main():
    parser = argparse.ArgumentParser(description='Spotify CLI - Control Spotify from the command line')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Now playing
    subparsers.add_parser('now', help='Show current playback')
    
    # Playback controls
    play_parser = subparsers.add_parser('play', help='Resume playback or play URI')
    play_parser.add_argument('uri', nargs='?', help='Spotify URI to play')
    play_parser.add_argument('--open', action='store_true', help='Open web player if no device found')
    
    subparsers.add_parser('pause', help='Pause playback')
    subparsers.add_parser('next', help='Next track')
    subparsers.add_parser('prev', help='Previous track')
    
    # Volume
    volume_parser = subparsers.add_parser('volume', help='Set volume (0-100)')
    volume_parser.add_argument('level', type=int, help='Volume level')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Search Spotify')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--type', choices=['track', 'artist', 'album'], default='track', help='Search type')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    
    # Playlists
    playlists_parser = subparsers.add_parser('playlists', help='List your playlists')
    playlists_parser.add_argument('--limit', type=int, default=20, help='Number of playlists')
    
    playlist_parser = subparsers.add_parser('playlist', help='Show playlist tracks')
    playlist_parser.add_argument('uri', help='Playlist URI')
    
    # Devices
    subparsers.add_parser('devices', help='List available devices')
    
    # Top tracks
    top_parser = subparsers.add_parser('top', help='Show top tracks')
    top_parser.add_argument('--limit', type=int, default=10, help='Number of tracks')
    top_parser.add_argument('--range', choices=['short', 'medium', 'long'], default='medium', 
                           help='Time range: short (4 weeks), medium (6 months), long (all time)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Check for credentials
    if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
        print("❌ Error: Spotify credentials not found!")
        print("\nCreate a .spotify-cli.env file in your home directory with:")
        print("SPOTIFY_CLIENT_ID=your_client_id")
        print("SPOTIFY_CLIENT_SECRET=your_client_secret")
        print("SPOTIFY_REDIRECT_URI=http://localhost:8888/callback")
        print(f"\nLocation: {os.path.join(os.path.expanduser('~'), '.spotify-cli.env')}")
        print("\nGet credentials at: https://developer.spotify.com/dashboard")
        sys.exit(1)

    try:
        cli = SpotifyCLI()
        
        if args.command == 'now':
            cli.current_playback()
        elif args.command == 'play':
            cli.play(args.uri, args.open)
        elif args.command == 'pause':
            cli.pause()
        elif args.command == 'next':
            cli.next_track()
        elif args.command == 'prev':
            cli.previous_track()
        elif args.command == 'volume':
            cli.volume(args.level)
        elif args.command == 'search':
            cli.search(args.query, args.type, args.limit)
        elif args.command == 'playlists':
            cli.my_playlists(args.limit)
        elif args.command == 'playlist':
            cli.playlist_tracks(args.uri)
        elif args.command == 'devices':
            cli.devices()
        elif args.command == 'top':
            time_range = f"{args.range}_term"
            cli.top_tracks(args.limit, time_range)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()