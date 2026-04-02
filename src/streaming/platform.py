"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from .tracks import Song, AlbumTrack
from .playlists import CollaborativePlaylist, Playlist
from collections import defaultdict
from datetime import datetime, timedelta
from .users import PremiumUser, FamilyMember



class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.tracks = {}
        self.users = {}
        self.artists = {}
        self.albums = {}
        self.playlists = {}
        self.sessions = []

    def add_track(self, track):
        self.tracks[track.track_id] = track

    def add_user(self, user):
        self.users[user.user_id] = user

    def add_artist(self, artist):
        self.artists[artist.artist_id] = artist

    def add_album(self, album):
        self.albums[album.album_id] = album

    def add_playlist(self, playlist):
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self.sessions.append(session)
        session.user.add_session(session)


    def all_users(self):
        return list(self.users.values())


    def total_listening_time_minutes(self, start, end):
        total_seconds = 0

        for session in self.sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60



    def avg_unique_tracks_per_premium_user(self, days=30):
        premium_users = [u for u in self.users if isinstance(u, PremiumUser)]
        if not premium_users:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)
        counts = []
        for user in premium_users:
            tracks = {
                s.track for s in user.sessions
                if s.timestamp >= cutoff
            }
            counts.append(len(tracks))

        return sum(counts) / len(counts)


    def track_with_most_distinct_listeners(self):
        if not self.sessions:
            return None
        listeners = defaultdict(set)

        for s in self.sessions:
            listeners[s.track].add(s.user)

        return max(listeners, key=lambda t: len(listeners[t]))


    def avg_session_duration_by_user_type(self):
        durations = defaultdict(list)

        for s in self.sessions:
            user_type = type(s.user).__name__
            durations[user_type].append(s.duration_listened_seconds)

        result = []
        for t, d in durations.items():
            result.append((t,sum(d) / len(d)))

        return sorted(result, key=lambda x: x[1], reverse=True)



    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total = 0
        for s in self.sessions:
            if isinstance(s.user, FamilyMember) and s.user.age < age_threshold:
                total += s.duration_listened_seconds
        return total / 60



    def top_artists_by_listening_time(self, n=5):
        artist_time = defaultdict(int)

        for s in self.sessions:
            if isinstance(s.track, Song):
                artist = s.track.artist
                artist_time[artist] += s.duration_listened_seconds

        ranked = sorted(
            [(a, t / 60) for a, t in artist_time.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:n]

    def user_top_genre(self, user_id):
        user = self.users.get(user_id)
        if user is None:
            return None

        genre_time = {}
        total_time = 0

        for session in user.sessions:
            if session.user_id == user_id:
                genre = session.track.genre
                seconds = session.duration_listened_seconds

                total_time += seconds
                genre_time[genre] = genre_time.get(genre, 0) + seconds


        if total_time == 0:
            return None

        top_genre = max(genre_time, key=genre_time.get)
        percentage = (genre_time[top_genre] / total_time) * 100

        return (top_genre, percentage)


    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []

        for p in self.playlists:
            if isinstance(p, CollaborativePlaylist):
                artists = {
                    t.artist for t in p.tracks if isinstance(t, Song)
                }
                if len(artists) > threshold:
                    result.append(p)

        return result


    def avg_tracks_per_playlist_type(self):
        types = {
            "Playlist": [],
            "CollaborativePlaylist": []
        }

        for p in self.playlists:
            types[type(p).__name__].append(len(p.tracks))

        return {
            k: (sum(v) / len(v) if v else 0.0)
            for k, v in types.items()
        }


    def users_who_completed_albums(self):
        album_tracks = defaultdict(set)

        for t in self.tracks:
            if isinstance(t, AlbumTrack) and t.album:
                album_tracks[t.album].add(t)

        results = []

        for user in self.users.values():
            listened = {s.track for s in user.sessions if s.user == user}
            completed = []

            for album, tracks in album_tracks.items():
                if tracks and tracks.issubset(listened):
                    completed.append(album.title)

            if completed:
                results.append((user, completed))

        return results


