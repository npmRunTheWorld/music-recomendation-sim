# [feature-001] Implement Core Music Recommender System

| Field | Value |
|---|---|
| Type | feature |
| Status | review |
| Impact | 5 |
| Effort | 3 |
| Priority | 1.67 |

## Description
Implement the full music recommender system including CSV loading, song scoring, ranking, OOP Recommender class, expanded song catalog, and documentation across all 5 phases.

## Requirements
| # | Requirement |
|---|---|
| 1 | `load_songs` reads data/songs.csv and returns list of dicts with correct types |
| 2 | `score_song` returns (float, List[str]) using genre, mood, energy, acousticness weights |
| 3 | `recommend_songs` ranks all songs and returns top-k |
| 4 | `Recommender.recommend` works with UserProfile and Song objects, sorted by score |
| 5 | `Recommender.explain_recommendation` returns non-empty string |
| 6 | songs.csv expanded with 5–10 diverse genres/moods |
| 7 | README.md documents system design and algorithm recipe |
| 8 | model_card.md completed |
| 9 | All tests pass |

## Acceptance Criteria
| # | Criteria | Pass? |
|---|---|---|
| 1 | `python3 -m src.main` prints top 5 recommendations with scores and reasons | ✅ |
| 2 | `pytest` passes both tests | ✅ |
| 3 | Three distinct user profiles produce different top-1 results | ✅ |
| 4 | README How The System Works section filled in | ✅ |
| 5 | model_card.md all sections completed | ✅ |

---

## Dev Notes
| Field | Value |
|---|---|
| Files Changed | src/recommender.py (full impl), src/main.py (3 profiles + clean output), data/songs.csv (+10 songs), README.md (system design), model_card.md (all 9 sections) |
| Edge Cases | Acousticness bonus applied to both acoustic and electric preferences; genre matching is case-insensitive; module import handles both `python3 src/main.py` and `python3 -m src.main` |

## QA
| Field | Value |
|---|---|
| Status | |
| Issues | |
| Over-engineered? | |
