from ytmusicapi import YTMusic


def search_track(
    search_query: str,
) -> (
    tuple[str, str, dict[str, str], list[dict[str, str]], list[dict[str, str]], str]
    | tuple[None, None, None, None, None, None]
):
    """
    Search for a track on YouTube Music with ytmusicapi for music-optimized search and no quota limits

    Args:
        search_query: Formatted query combining song name and primary artist

    Returns:
        Six-element tuple with track metadata or None values for failed searches

    Reference:
        https://ytmusicapi.readthedocs.io/en/stable/usage.html
    """

    try:
        # Initialize YouTube Music client
        ytmusic = YTMusic()

        # Execute search with music-specific filtering
        track = ytmusic.search(search_query, filter="songs", limit=1)

        # Extract metadata
        if track and len(track) > 0:
            video_id = track[0]["videoId"]
            title = track[0]["title"]
            thumbnails = track[0]["thumbnails"]
            artists = track[0]["artists"]
            album = track[0]["album"]
            length = track[0]["duration"]
            print(
                f"   ✅ Found: {title} - {', '.join([artist['name'] for artist in artists])}\n"
            )
            return video_id, title, thumbnails, artists, album, length

        else:
            print(f"   ❌ No results for: {search_query}\n")
            return None, None, None, None, None, None

    except Exception as e:
        print(f"   ❌ Error searching YouTube: {e}\n")
        return None, None, None, None, None, None
