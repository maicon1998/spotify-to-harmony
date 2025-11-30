import json
from typing import Any


class HarmonyPlaylist:
    """
    Load, add tracks and export to Harmony playlist.

    Attributes:
        filename (str): Harmony playlist template file
        data (dict[str, Any]): The loaded playlist data structure
        is_loaded (bool): Whether the template has been successfully loaded
    """

    def __init__(self, filename: str) -> None:
        """
        Initialize HarmonyPlaylist with a template file.

        Args:
            filename: Filename of Harmony Music JSON template file
        """
        self.filename = filename
        self.data = None
        self.is_loaded = False

    def load_template(self) -> bool:
        """
        Load Harmony Music playlist template from JSON file.

        Returns:
            bool: True if template was loaded successfully, False otherwise

        Raises:
            FileNotFoundError: When template file doesn't exist
            JSONDecodeError: When template file contains invalid JSON
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            self.is_loaded = True
            print(f"✅ Loaded Harmony template: {self.filename}\n")
            return True

        except FileNotFoundError:
            print(f"❌ Template file not found: {self.filename}\n")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in template file: {e}\n")
            return False
        except Exception as e:
            print(f"❌ Error reading template file: {e}\n")
            return False

    def add_track(self, track_data: dict[str, Any]) -> bool:
        """
        Add a track to the playlist.

        Args:
            track_data: Dictionary containing track metadata in Harmony Music format

        Returns:
            bool: True if track was added successfully, False otherwise

        Note:
            Required fields or will not work: videoId, title and thumbnails
        """
        if not self.is_loaded or self.data is None:
            print("❌ Playlist not loaded. Call load_template() first.\n")
            return False

        try:
            self.data["songs"].append(track_data)
            return True
        except KeyError:
            print("❌ Invalid playlist structure: 'songs' key not found\n")
            return False
        except Exception as e:
            print(f"❌ Error adding track: {e}\n")
            return False

    def save(self, output_filename="harmony_playlist.json") -> bool:
        """
        Save the playlist to a JSON file.

        Args:
            output_filename: output filename.

        Returns:
            bool: True if save was successful, False otherwise
        """
        if not self.is_loaded or self.data is None:
            print("❌ No playlist data to save. Call load_template() first.\n")
            return False

        try:
            with open(output_filename, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            print(f"💾 Harmony playlist saved: {output_filename}\n")
            return True
        except Exception as e:
            print(f"❌ Error saving playlist: {e}\n")
            return False

    def create_track_dict(
        self,
        video_id: str,
        title: str,
        thumbnails: list[dict[str, str]],
        artists: str | None = None,
        album: dict[str, str] | None = None,
        length: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a properly formatted track dictionary for Harmony Music.

        Args:
            video_id: YouTube video ID
            title: Track title
            thumbnails: Thumbnail URLs and dimensions
            artists: Artist or artists names
            album: Album art
            length: Track duration

        Returns:
            Dictionary in Harmony Music track format
        """
        return {
            "videoId": video_id,
            "title": title,
            "album": album,
            "artists": artists,
            "length": length,
            "duration": None,
            "date": None,
            "thumbnails": thumbnails,
            "url": None,
            "trackDetails": None,
            "year": None,
        }
