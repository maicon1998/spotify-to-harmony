from dotenv import load_dotenv
import os
import base64
from requests import post, get
import time
import json
from datetime import datetime

load_dotenv()

spotify_id = os.getenv("SPOTIFY_ID")
spotify_secret = os.getenv("SPOTIFY_SECRET")
spotify_token_cache = "spotify_token_cache.json"


def get_token() -> str | None:
    """
    Get Spotify access token using Client Credentials flow.

    Returns:
        str | None: Access token if successful, None if authentication failed

    Reference:
        https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
    """

    # Check for valid cached token first to avoid unnecessary API calls
    if os.path.exists(spotify_token_cache):
        try:
            with open(spotify_token_cache, "r") as f:
                cache_data = json.load(f)

            # Check if token hasn't expired yet (with safety buffer)
            expires_at = cache_data.get("expires_at")
            if expires_at and time.time() < expires_at - 300:
                print("♻️ Using cached Spotify token\n")
                return cache_data["access_token"]

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Cache corruted or key missing: {e}, getting new token\n")

    # Encode credentials for Spotify Client Credentials Flow
    print("🔄 Getting new Spotify token...\n")
    auth_string = f"{spotify_id}:{spotify_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Request config for OAuth 2.0
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    # Token request
    try:
        response = post(url, headers=headers, data=data)
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        json_response = response.json()

        # Cache the token to reduce API calls and avoid hitting rate limits
        cache_data = {
            "access_token": json_response["access_token"],
            "expires_at": time.time() + json_response["expires_in"],
            "token_type": json_response["token_type"],
            "cached_at": datetime.now().isoformat(),
        }

        with open(spotify_token_cache, "w") as f:
            json.dump(cache_data, f, indent=2)

        print("✅ New Spotify token cached\n")
        return json_response["access_token"]

    except Exception as e:
        print(f"❌ Error getting Spotify token: {e}\n")
        return None


def get_auth_header(token: str) -> dict[str, str]:
    """Create Authorization header for Spotify API requests.

    Returns:
        Dictionary with Authorization header
    """

    return {"Authorization": "Bearer " + token}


def get_all_playlist_tracks(token: str, playlist_id: str) -> list:
    """
    Retrieve all tracks from a Spotify playlist with pagination.

    Args:
        token: Spotify access token
        playlist_id: ID of the Spotify playlist to fetch

    Returns:
        List of track dictionaries with song name, artist and search query

    Reference:
        https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks
    """

    all_tracks = []
    limit = 50  # Spotify's maximum items per page
    offset = 0

    # Paginate through all tracks until complete
    while True:
        try:
            # API endpoint with pagination parameters
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            query = f"?limit={limit}&offset={offset}"
            headers = get_auth_header(token)

            response = get(url + query, headers=headers)
            response.raise_for_status()  # Raises exception for 4xx/5xx status codes
            json_response = response.json()

            # Validate response structure
            if "items" not in json_response:
                print("❌ Unexpected API response format from Spotify\n")
                break

            if not json_response["items"]:
                print("✅ Reached end of playlist\n")
                break  # No more tracks to process

            # Process tracks in current page
            batch_tracks = []
            for item in json_response["items"]:
                track = item["track"]
                if track:
                    song_name = track["name"]
                    artist = track["artists"][0]["name"]
                    batch_tracks.append(
                        {
                            "song_name": song_name,
                            "artist": artist,
                            "search_query": f"{song_name} {artist}",
                        }
                    )

            # Add this batch to our complete list
            all_tracks.extend(batch_tracks)
            print(
                f"📥 Retrieved {len(batch_tracks)} tracks... Total: {len(all_tracks)}"
            )

            # Exit loop when it reaches the last page
            if len(batch_tracks) < limit:
                break

            offset += limit  # Next page
            time.sleep(0.1)  # Delay to avoid rate limiting

        except Exception as e:
            print(f"❌ Error fetching Spotify tracks (offset {offset}): {e}\n")
            break

    return all_tracks
