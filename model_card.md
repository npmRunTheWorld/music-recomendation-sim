# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's preferred genre, mood, energy level, and whether they prefer acoustic or electric sounds. It is built for classroom exploration — to demonstrate how a content-based recommender works under the hood. It is not intended for real-world deployment or production use.

---

## 3. How the Model Works

Every song in the catalog gets a numeric score compared to the user's taste profile. The scoring works like a point system:

- **Genre match** is worth the most — 2 full points if the song's genre matches the user's favorite.
- **Mood match** adds 1 point if the song's mood matches (e.g., "chill," "intense," "happy").
- **Energy similarity** adds up to 1 point based on how close the song's energy level is to the user's target. A perfect match gives 1.0; a song at the opposite extreme gives 0.0.
- **Acoustic preference** adds up to 0.5 points — more if the user likes acoustic music and the song is acoustic, or more if the user prefers electric sounds and the song is electric.

Once every song has a score, the system sorts them from highest to lowest and returns the top results.

---

## 4. Data

The catalog contains 20 songs. Genres represented include: pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, acoustic, folk, and r&b. Moods include: happy, chill, intense, relaxed, moody, and focused.

Ten songs were present in the starter dataset; ten were added to increase diversity across genres and moods. The dataset is small and skewed toward electronic and pop styles — classical, hip-hop, country, and world music are not represented.

---

## 5. Strengths

- Works well for users with a clear genre preference. The 2-point genre bonus makes genre the strongest signal, so listeners who primarily care about genre get consistent results.
- Transparent and explainable. Every recommendation includes a plain-English reason for each point added.
- Fast and deterministic. With 20 songs it runs instantly and always produces the same result for the same input.
- Three very different user profiles (Pop, Lofi, Rock) all produce distinct top-1 recommendations with no overlap.

---

## 6. Limitations and Bias

- **Genre dominance.** A 2-point genre bonus means a genre match almost always beats non-matching songs, even if mood and energy are perfect. A great chill jazz track will always lose to a mediocre lofi track for a "lofi" user.
- **Small catalog.** With only 20 songs, the system quickly runs out of variety — especially for niche genres like jazz or folk.
- **No collaborative signal.** The system has no idea what other listeners enjoy. Real platforms like Spotify blend content signals with "people who liked X also liked Y."
- **Binary genre matching.** "indie pop" and "pop" are treated as completely different. The system cannot recognize that they are related.
- **Filter bubble risk.** The heavy genre weight means users rarely discover music outside their stated genre — even if a song in another genre perfectly matches their energy and mood.
- **Underrepresented moods.** Moods like "focused" and "moody" appear in only 1–2 songs each, so users with those preferences get little variety.

---

## 7. Evaluation

Three user profiles were tested:

1. **High-Energy Pop Fan** (genre: pop, mood: happy, energy: 0.85, electric): Top result was *Sunrise City* with score 4.38. The pop + happy + high energy combination matched well. Second pick, *Gym Hero*, scored 3.40 — pop match but mood was "intense" instead of "happy," showing mood does matter.

2. **Chill Lofi Listener** (genre: lofi, mood: chill, energy: 0.38, acoustic): Top two were *Library Rain* and *Midnight Coding* — both lofi + chill + low energy. The acoustic bonus pushed them above *Focus Flow* (lofi but "focused" mood). This felt correct.

3. **Intense Rock Head** (genre: rock, mood: intense, energy: 0.90, electric): *Storm Runner* and *Fire Season* tied closely at ~4.4. Both rock + intense + high energy. Third place was *Desert Pulse* (electronic/intense) — not rock, but the mood and energy pulled it up. This is a reasonable "discovery" result.

No profile shared a top-3 result, confirming the profiles are differentiated. A surprise: electronic/intense tracks often appear in the Rock Head profile's lower ranks because energy and mood overlap, even though the genre differs. This shows the scoring can surface cross-genre discoveries when genre doesn't match but other features do.

---

## 8. Future Work

- **Increase genre weight granularity.** Use genre similarity (e.g., a "genre family" tree) instead of exact string matching so "indie pop" gets partial credit for a "pop" user.
- **Add a diversity penalty.** Prevent the same artist from appearing more than once in the top 5, to avoid redundancy.
- **Collaborative filtering layer.** Track which profiles agree on songs and use that to surface surprises — "users like you also enjoyed this ambient track."
- **Expand the catalog.** Add 50+ songs covering classical, hip-hop, country, and world music to reduce filter bubble risk.
- **Tempo preference.** Allow users to specify a preferred tempo range (e.g., 60–90 BPM for relaxed sessions) and score tempo similarity similarly to energy.

---

## 9. Personal Reflection

Building this made it clear how much a simple weighting scheme can already "feel smart." The three profiles produce genuinely different, intuitive results — even though the algorithm is just arithmetic. The most interesting discovery was the genre dominance problem: a 2-point genre bonus is so strong it almost always wins, which means the system is really a genre filter with mood and energy as tiebreakers. Real recommenders must have solved this, perhaps by normalizing scores across features or using learned weights rather than hand-tuned ones. It also highlighted how a small dataset creates a ceiling — once you use all the genre-matching songs, the system is just ranking the rest by energy proximity. That ceiling disappears when you have millions of tracks, which explains why Spotify recommendations feel so much richer.
