"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

class Track:
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number, album=None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = album

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host=None, description=""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title,  duration_seconds, genre, host, guest):
        super().__init__(track_id, title, duration_seconds, genre, host)
        self.guest = guest

class NarrativeEpisode(Podcast):

    def __init__(self, track_id, title, duration_seconds, genre, season, episode_number, host, description=None):
        super().__init__(track_id, title, duration_seconds, genre, host)
        self.season = season
        self.episode_number = episode_number
        self.description = description


class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator


