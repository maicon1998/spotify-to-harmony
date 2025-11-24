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


def get_token():
    """https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow"""

    if os.path.exists(spotify_token_cache):
        try:
            with open(spotify_token_cache, "r") as f:
                cache_data = json.load(f)

            expires_at = cache_data.get("expires_at")
            if expires_at and time.time() < expires_at - 300:
                print("♻️ Using cached Spotify token\n")
                return cache_data["access_token"]

        except (json.JSONDecodeError, KeyError) as e:
            print("⚠️ Cache corrupted, getting new token\n")

    print("🔄 Getting new Spotify token...\n")
    auth_string = spotify_id + ":" + spotify_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = post(url, headers=headers, data=data)
        response.raise_for_status()
        json_response = response.json()

        # Cache the token to prevent unnecessary API calls and avoid hitting rate limits
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


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_all_playlist_tracks(token, playlist_id):
    """https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks"""
    all_tracks = []
    limit = 50
    offset = 0

    while True:
        try:
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            query = f"?limit={limit}&offset={offset}"
            headers = get_auth_header(token)

            response = get(url + query, headers=headers)
            json_response = response.json()

            if "items" not in json_response or not json_response["items"]:
                print("❌ Unexpected response from Spotify\n")
                break

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

            all_tracks.extend(batch_tracks)
            print(f"Retrieved {len(batch_tracks)} tracks... Total: {len(all_tracks)}\n")

            # Break the loop when it reaches the last page
            if len(batch_tracks) < limit:
                break

            offset += limit  # Next page
            time.sleep(0.1)  # Delay to avoid rate limiting

        except Exception as e:
            print(f"❌ Error fetching Spotify tracks (offset {offset}): {e}\n")
            break

    return all_tracks
