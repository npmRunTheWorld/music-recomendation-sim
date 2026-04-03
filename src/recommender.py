import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommender that scores and ranks Song objects against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        score += energy_similarity
        reasons.append(f"energy similarity (+{energy_similarity:.2f})")

        if user.likes_acoustic:
            score += song.acousticness * 0.5
            reasons.append(f"acoustic bonus (+{song.acousticness * 0.5:.2f})")
        else:
            score += (1.0 - song.acousticness) * 0.5
            reasons.append(f"electric bonus (+{(1.0 - song.acousticness) * 0.5:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs sorted by score descending."""
        scored = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        _, reasons = self._score(user, song)
        return ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score, reasons).

    Algorithm Recipe:
      +2.0  genre match
      +1.0  mood match
      +0..1 energy similarity (1 - |song_energy - target_energy|)
      +0..0.5 acoustic/electric preference bonus
    """
    score = 0.0
    reasons = []

    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_similarity = 1.0 - abs(song["energy"] - target_energy)
    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        bonus = song["acousticness"] * 0.5
        score += bonus
        reasons.append(f"acoustic bonus (+{bonus:.2f})")
    else:
        bonus = (1.0 - song["acousticness"]) * 0.5
        score += bonus
        reasons.append(f"electric bonus (+{bonus:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank them, and return top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
