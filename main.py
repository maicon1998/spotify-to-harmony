from spotify.api import get_token, get_all_playlist_tracks
from ytmusic.search import search_track
from harmony.harmony_manager import HarmonyPlaylist
import json


def main() -> None:
    """
    Main entry point for Spotify to Harmony Music playlist converter.

    Workflow:
        1. Authenticates with Spotify API
        2. Fetches playlist tracks from Spotify
        3. Searches for equivalent tracks on YouTube Music
        4. Builds Harmony Music compatible JSON playlist

    Example:
        $ python main.py
        Enter Spotify playlist ID: 37i9dQZF1Eexample
        Enter Harmony playlist template: empty_playlist.json
        ✅ Successfully converted 150/150 tracks

    Note:
        Requires pre-configured Spotify developer credentials in .env file
        and an empty Harmony Music playlist template for formatting.
    """

    print("🎵 Spotify to Harmony Music Playlist converter\n")

    # Spotify Authentication
    # Get access token for Spotify Web API using Client Credentials Flow
    print("🔐 Getting Spotify access token...\n")
    token = get_token()
    if not token:
        print("❌ Spotify authentication failed.\n")
        return

    # User input
    # Get source Spotify playlist and target Harmony template
    playlist_id = input("Enter Spotify playlist ID: ").strip()
    harmony_template_file = input(
        "Enter name of harmony playlist template (e.g., empty_playlist.json): "
    ).strip()

    # Harmony template
    # Initialize and load Harmony playlist
    harmony = HarmonyPlaylist(harmony_template_file)
    if not harmony.load_template():
        return  # Template loading failed

    # Spotify playlist
    # Fetch all tracks from specified Spotify playlist with pagination
    print("\n📀 Fetching tracks from Spotify...\n")
    all_tracks = get_all_playlist_tracks(token, playlist_id)

    if not all_tracks:
        print("❌ No tracks found or error fetching from Spotify.\n")
        return

    print(f"🎵 Found {len(all_tracks)} tracks in Spotify playlist\n")

    # Track Search and Conversion
    # For each Spotify track, search YouTube Music and add to Harmony playlist
    print("🔍 Searching for tracks on YouTube Music...\n")
    successful_adds = 0
    failed_searches = []

    for i, track in enumerate(all_tracks, 1):
        print(f"{i}/{len(all_tracks)}: Searching '{track['song_name']}'...\n")

        # Search YouTube Music for equivalent track
        video_id, title, thumbnails, artists, album, length = search_track(
            track["search_query"]
        )

        if video_id and title and thumbnails:
            track_dict = harmony.create_track_dict(
                video_id=video_id,
                title=title,
                thumbnails=thumbnails,
                artists=artists,
                album=album,
                length=length,
            )

            harmony.add_track(track_dict)
            successful_adds += 1

        else:
            # Track search failed - log for manual review
            print(f"   ❌ Not found: {track}\n")
            failed_searches.append(track)

    # Save the playlist
    harmony.save()

    # Summary
    print("🎉 Conversion Complete!\n")
    print(f"✅ Successfully added: {successful_adds}/{len(all_tracks)} tracks\n")
    print(f"❌ Failed to find/add: {len(failed_searches)} tracks\n")
    print("📁 Output file: harmony_playlist.json")

    # Save failed tracks to file for manual review
    if failed_searches:
        print("Failed tracks:\n")
        for track in failed_searches:
            print(f"  - {track['song_name']} - {track['artist']}")

        with open("failed_tracks.json", "w", encoding="utf-8") as f:
            json.dump(failed_searches, f, indent=2, ensure_ascii=False)
        print("Failed tracks saved to 'failed_tracks.json'\n")


if __name__ == "__main__":
    main()
