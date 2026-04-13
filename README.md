# Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender I built to understand how real recommendation systems actually work under the hood. It scores songs against a user taste profile using four weighted features: genre, mood, energy, and acoustic preference. It ranks a catalog of 20 songs, explains every recommendation in plain English, and supports multiple distinct user profiles — each producing different top results. Building this made it clear how quickly a simple scoring rule starts to feel "smart" even when it's just arithmetic.

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

Genre match dominates (worth 2× any other signal), so this system is really a genre filter with mood and energy as tiebreakers. Songs outside the user's genre rarely reach the top unless the catalog has no genre match at all. I noticed this during testing — a great chill jazz track will always lose to a mediocre lofi track for a "lofi" user, no matter how well everything else lines up.

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
streamlit run src/app.py
```

### Run CLI (no UI)

```bash
python3 -m src.main
```

### Run tests

```bash
python3 -m pytest
```

---

## Sample Terminal Output

Running the CLI with the three default profiles:

```
Loaded 20 songs.

==================================================
  Profile: High-Energy Pop Fan
==================================================
  1. Sunrise City by Neon Echo
     Score : 4.38
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.97), electric bonus (+0.41)
  2. Gym Hero by Max Pulse
     Score : 3.40
     Why   : genre match (+2.0), energy similarity (+0.92), electric bonus (+0.47)
  3. Rooftop Lights by Indigo Parade
     Score : 2.24
     Why   : mood match (+1.0), energy similarity (+0.91), electric bonus (+0.33)
  4. Sunday Slow by Petal Soft
     Score : 1.93
     Why   : mood match (+1.0), energy similarity (+0.70), electric bonus (+0.22)
  5. Morning Stretch by Calm Hands
     Score : 1.66
     Why   : mood match (+1.0), energy similarity (+0.60), electric bonus (+0.06)

==================================================
  Profile: Chill Lofi Listener
==================================================
  1. Library Rain by Paper Lanterns
     Score : 4.40
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.97), acoustic bonus (+0.43)
  2. Midnight Coding by LoRoom
     Score : 4.31
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.96), acoustic bonus (+0.35)
  3. Focus Flow by LoRoom
     Score : 3.37
     Why   : genre match (+2.0), energy similarity (+0.98), acoustic bonus (+0.39)
  4. Spacewalk Thoughts by Orbit Bloom
     Score : 2.36
     Why   : mood match (+1.0), energy similarity (+0.90), acoustic bonus (+0.46)
  5. Breathe Out by Still Waters
     Score : 2.31
     Why   : mood match (+1.0), energy similarity (+0.84), acoustic bonus (+0.47)

==================================================
  Profile: Intense Rock Head
==================================================
  1. Storm Runner by Voltline
     Score : 4.44
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.99), electric bonus (+0.45)
  2. Fire Season by Ember Red
     Score : 4.41
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.97), electric bonus (+0.44)
  3. Desert Pulse by Sand & Static
     Score : 2.46
     Why   : mood match (+1.0), energy similarity (+0.98), electric bonus (+0.48)
  4. Gym Hero by Max Pulse
     Score : 2.44
     Why   : mood match (+1.0), energy similarity (+0.97), electric bonus (+0.47)
  5. Bass Drop Protocol by Circuit Nine
     Score : 2.44
     Why   : mood match (+1.0), energy similarity (+0.95), electric bonus (+0.49)
```

Zero overlap in the top 5 across all three profiles, which is a good sign the scoring is actually differentiating between them. The rock head's #3 is *Desert Pulse* (electronic) — not rock, but intense + high energy + electric, so it bubbles up when the genre pool runs dry.

---

## Experiments

### Weight Shift: What if genre weight doubles?
Genre already dominates at 2.0 points. I tried bumping it to 4.0 and it completely killed cross-genre discovery — any genre match would outscore a near-perfect mood+energy match by a factor of 2. The system basically became a genre lookup with some noise. Not useful.

### Feature Removal: Remove mood check
Without the mood bonus, *Gym Hero* (pop, intense) scores nearly as high as *Sunrise City* (pop, happy) for a "happy pop" user — only energy and acoustic preference separate them. Mood is doing real work as a tiebreaker, but since it's worth half the genre weight, it's still the second-string signal.

### Profile Comparison
- **EDM profile** (electronic, intense, energy 0.90) → top results: *Desert Pulse*, *Neon Jungle*, *Bass Drop Protocol*
- **Acoustic profile** (acoustic, relaxed, energy 0.30) → top results: *Rainy Bookshelf*, *The Long Way Home*, *Morning Stretch*

Almost no overlap between these two. Energy and acoustic preference together create a strong enough divide that even songs in the same mood category land in completely different rank positions.

See [reflection.md](reflection.md) for a deeper comparison of the profiles.

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

The biggest thing I learned building this is how much a genre filter *feels* like a real recommender, even when it's basically just sorting. The three profiles produce results that make intuitive sense — but mostly because genres are different, not because the algorithm is doing anything clever.

The genre dominance problem is the main thing I'd fix. Hand-tuned weights are too brittle; learned weights from real listening data would be way more accurate. Real platforms like Spotify must be doing something much more nuanced, probably normalizing scores per user rather than using global weights.

I also hit the small dataset ceiling fast — once all the genre-matching songs are ranked, you're just sorting the rest by energy proximity. That ceiling disappears with a large catalog, which explains why Spotify discovery gets better the more you listen.

For a deeper profile-to-profile comparison see [reflection.md](reflection.md), and for the full bias/evaluation breakdown see the [Model Card](model_card.md).
