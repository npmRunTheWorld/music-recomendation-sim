# Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender that scores songs against a user taste profile using four weighted features: genre, mood, energy, and acoustic preference. It ranks a catalog of 20 songs, explains every recommendation in plain English, and supports multiple distinct user profiles — each producing different top results. The project demonstrates how real-world recommenders turn structured data into ranked suggestions, and exposes where simple scoring rules fall short.

---

## How The System Works

### Real-World Context

Platforms like Spotify use two main strategies. **Content-based filtering** scores songs by their attributes (tempo, mood, energy) against a user's known preferences. **Collaborative filtering** finds users with similar listening histories and surfaces what they liked. VibeFinder uses only content-based filtering — no listening history, just feature matching.

### Algorithm Recipe

Each song gets a numeric score calculated as:

| Signal | Points |
|---|---|
| Genre match (exact) | +2.0 |
| Mood match (exact) | +1.0 |
| Energy similarity | +0.0 to +1.0 (1 - \|song_energy - target_energy\|) |
| Acoustic/electric preference | +0.0 to +0.5 (acousticness × 0.5 or inverse) |

**Max possible score: 4.5.** Songs are sorted highest-to-lowest; top-k are returned.

### Data Flow

```
User Taste Profile (genre, mood, energy, likes_acoustic)
        ↓
For each song in catalog (20 songs in data/songs.csv)
        ↓
  score_song() → (numeric score, list of reasons)
        ↓
Sort all (song, score, reasons) by score descending
        ↓
Return top-k recommendations with explanations
```

### Song Features Used

- `genre` — string (pop, rock, lofi, electronic, etc.)
- `mood` — string (happy, chill, intense, relaxed, moody, focused)
- `energy` — float 0.0–1.0
- `acousticness` — float 0.0–1.0

### User Profile Fields

- `genre` — favorite genre (string)
- `mood` — favorite mood (string)
- `energy` — target energy level (float 0.0–1.0)
- `likes_acoustic` — bool (True → prefer acoustic, False → prefer electric)

### Expected Bias

Genre match dominates (worth 2× any other signal), so this system is really a genre filter with mood and energy as tiebreakers. Songs outside the user's genre rarely reach the top unless the catalog has no genre match at all.

---

## Getting Started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the app

```bash
python3 -m src.main
```

### Run tests

```bash
python3 -m pytest
```

---

## Experiments

### Weight Shift: What if genre weight doubles?
Genre already dominates at 2.0 points. Raising it to 4.0 would completely eliminate cross-genre discovery — any genre match would outscore a near-perfect mood+energy match by a factor of 2. The system would degrade to a pure genre filter.

### Feature Removal: Remove mood check
Without the mood bonus, *Gym Hero* (pop, intense) scores nearly as high as *Sunrise City* (pop, happy) for a "happy pop" user — only energy and acoustic preference separate them. Mood is a meaningful tiebreaker, but the difference is small (~1 point) compared to genre (2 points).

### Profile Comparison
- **EDM profile** (electronic, intense, energy 0.90) → surfaces *Desert Pulse*, *Neon Jungle*, *Bass Drop Protocol*
- **Acoustic profile** (acoustic, relaxed, energy 0.30) → surfaces *Rainy Bookshelf*, *The Long Way Home*, *Morning Stretch*

The outputs are almost completely non-overlapping. Energy and acoustic preference create a clear divide even within the same mood category.

---

## Limitations and Risks

- Only 20 songs — genre variety runs out quickly
- No collaborative signal — ignores what similar listeners enjoy
- Binary genre matching — "indie pop" ≠ "pop" even though they overlap
- Heavy genre weight creates a filter bubble
- No understanding of lyrics, language, or cultural context

See the [Model Card](model_card.md) for full analysis.

---

## Reflection

See [Model Card → Personal Reflection](model_card.md#9-personal-reflection).
