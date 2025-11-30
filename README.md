## Demo
https://github.com/user-attachments/assets/949e3fa2-f1fc-42a6-8bb7-afa748db50c9

# 🎵 Spotify to Harmony Music Playlist Converter

A  Python tool that converts Spotify playlists into [Harmony Music](https://github.com/anandnet/Harmony-Music) importable JSON files by searching for tracks on YouTube Music.

## ✨ Features

- **No YouTube API Quota Limits** - Uses ytmusicapi for unlimited searches
- **Accurate Music Matching** - YouTube Music's specialized search algorithm
- **Portable Playlists** - Create Harmony Music JSON files for easy import
- **Efficient** - Processes large playlists without API restrictions
- **Metadata** - Captures album art, artist info, and track details

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Spotify Developer Account
- Harmony Music app

### Installation

```bash

# Clone the repository
git clone https://github.com/maicon1998/spotify-to-harmony.git
cd spotify-to-harmony

# Install dependencies
pip install -r requirements.txt
```

## 📈 Project Journey

You can import your YouTube playlists by copying the playlist link and pasting it into the Harmony search bar, clicking on the 3 dots (show menu) and add songs to playlist.

The first attempt was to convert Spotify playlists to YouTube playlists. The problem was the limitation of 10000 daily quotas using YouTube API.

So I tried three distinct architectures, each solving critical limitations of the previous approach:

### **Version 1: Pure YouTube Data API** 🟥 *Limited*

 - Architecture: Spotify → YouTube Data API → YouTube Playlist
 - Quota Impact: 100 searches = 10000 quota (entire daily limit!)

### **Version 2: Hybrid Approach** 🟨 *Better*

- Architecture: Spotify → ytmusicapi (search) → YouTube Data API (playlist)
- Quota Impact: 200 inserts = 10000 quota  
- Maximum Playlist: ~200 tracks per day

### **Version 3: Harmony Music Export** 🟩 *Unlimited*

- Architecture: Spotify → ytmusicapi (search) → Harmony JSON File
- Quota Impact: ZERO - no YouTube API calls
- Maximum Playlist: Unlimited tracks in one run
