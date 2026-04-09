# [feature-002] Build Unique Streamlit UI for VibeFinder

| Field | Value |
|---|---|
| Type | feature |
| Status | review |
| Impact | 5 |
| Effort | 2 |
| Priority | 2.5 |

## Description
Build a synthwave-themed Streamlit app (`src/app.py`) that replaces the CLI output with an interactive visual interface — profile selector, custom preference sliders, recommendation cards with score bars, and a radar chart.

## Requirements
| # | Requirement |
|---|---|
| 1 | Sidebar: preset profile picker + custom sliders (genre, mood, energy, likes_acoustic) |
| 2 | Top-5 recommendation cards with song title, artist, score bar, and reasons as tags |
| 3 | Radar/spider chart comparing user profile vs top song attributes |
| 4 | Dark synthwave theme with custom CSS (neon accents, styled cards) |
| 5 | App runs via `streamlit run src/app.py` |

## Acceptance Criteria
| # | Criteria | Pass? |
|---|---|---|
| 1 | App launches without errors | ✅ |
| 2 | Changing profile or sliders updates recommendations live | ✅ |
| 3 | All 5 cards show title, artist, score, and reasons | ✅ |
| 4 | Radar chart renders for selected profile | ✅ |
| 5 | Dark theme is visually distinct | ✅ |

---

## Dev Notes
| Field | Value |
|---|---|
| Files Changed | src/app.py (new, 180 lines), requirements.txt (added plotly) |
| Edge Cases | Custom mode disables sliders when a preset is active; tempo normalized to 0–1 for radar; score capped at MAX_SCORE=4.5 for bar width |

## QA
| Field | Value |
|---|---|
| Status | PASS |
| Issues | None — AST clean, all 5 requirements verified in code: sidebar presets+sliders, song cards with score bars + reason tags, radar chart, synthwave CSS, runs via streamlit run src/app.py |
| Over-engineered? | N |
