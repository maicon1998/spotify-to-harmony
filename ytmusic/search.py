from ytmusicapi import YTMusic


def search_track(search_query):
    try:
        ytmusic = YTMusic()
        track = ytmusic.search(search_query, filter="songs", limit=1)

        if track and len(track) > 0:
            video_id = track[0]["videoId"]
            title = track[0]["title"]
            artists = track[0]["artists"]
            album = track[0]["album"]
            thumbnails = track[0]["thumbnails"]
            print(
                f"   ✅ Found: {title} - {', '.join([artist['name'] for artist in artists])}\n"
            )
            return video_id, title, album, artists, thumbnails

        else:
            print(f"   ❌ No results for: {search_query}\n")
        return None, None, None, None, None

    except Exception as e:
        print(f"   ❌ Error searching YouTube: {e}\n")
        return None, None, None, None, None
