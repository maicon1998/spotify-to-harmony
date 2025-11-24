from spotify.api import get_token, get_all_playlist_tracks
from ytmusic.search import search_track
import json


def main():
    print("🎵 Spotify to Harmony Music Playlist Converter\n")

    print("🎵 Getting Spotify access token...\n")
    token = get_token()
    if not token:
        print("❌ Spotify authentication failed.\n")
        return

    # User input
    playlist_id = input("Enter Spotify playlist ID: ").strip()
    harmony_template_file = input(
        "Enter name of harmony playlist template (e.g., empty_playlist.json): "
    ).strip()

    # Load harmony template
    try:
        with open(harmony_template_file, "r", encoding="utf-8") as f:
            harmony_data = json.load(f)
        print(f"✅ Loaded Harmony template: {harmony_template_file}\n")
    except FileNotFoundError:
        print(f"❌ File not found: {harmony_template_file}\n")
        return
    except Exception as e:
        print(f"❌ Error reading template file: {e}\n")
        return

    print("📀 Fetching tracks from Spotify...\n")
    all_tracks = get_all_playlist_tracks(token, playlist_id)

    if not all_tracks:
        print("❌ No tracks found or error fetching from Spotify.\n")
        return

    print(f"🎵 Found {len(all_tracks)} tracks in Spotify playlist\n")

    print("🔍 Searching for tracks on YouTube Music...\n")
    successful_adds = 0
    failed_searches = []

    for i, track in enumerate(all_tracks, 1):
        print(f"{i}/{len(all_tracks)}: Searching '{track['song_name']}'...\n")

        video_id, title, album, artists, thumbnails = search_track(
            track["search_query"]
        )

        if video_id:
            # Add to harmony playlist
            harmony_data["songs"].append(
                {
                    "videoId": video_id,
                    "title": title,
                    "album": album,
                    "artists": artists,
                    "length": None,
                    "duration": None,
                    "date": None,
                    "thumbnails": thumbnails,
                    "url": None,
                    "trackDetails": None,
                    "year": None,
                }
            )
            successful_adds += 1

        else:
            print(f"   ❌ Not found: {track}\n")
            failed_searches.append(track)

    output_filename = "harmony_playlist.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(harmony_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Harmony playlist saved as: {output_filename}\n")
    except Exception as e:
        print(f"❌ Error saving playlist: {e}\n")

    # Summary
    print("🎉 Migration Complete!\n")
    print(f"✅ Successfully added: {successful_adds}/{len(all_tracks)} tracks\n")
    print(f"❌ Failed to find/add: {len(failed_searches)} tracks\n")

    if failed_searches:
        print("Failed tracks:\n")
        for track in failed_searches:
            print(f"  - {track['song_name']} - {track['artist']}")

        # Save failed tracks to file
        with open("failed_tracks.json", "w", encoding="utf-8") as f:
            json.dump(failed_searches, f, indent=2, ensure_ascii=False)
        print("Failed tracks saved to 'failed_tracks.json'\n")


if __name__ == "__main__":
    main()
