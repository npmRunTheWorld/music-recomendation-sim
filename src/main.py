"""
Command line runner for the Music Recommender Simulation.
Demonstrates three distinct user profiles to evaluate the recommender.
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Intense Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
        "likes_acoustic": False,
    },
}


def print_recommendations(profile_name: str, recommendations) -> None:
    print(f"\n{'='*50}")
    print(f"  Profile: {profile_name}")
    print(f"{'='*50}")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recommendations)

    print()


if __name__ == "__main__":
    main()
