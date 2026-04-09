"""
VibeFinder 1.0 — Streamlit UI
Synthwave-themed interactive music recommender.
"""

import streamlit as st
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.recommender import load_songs, recommend_songs, score_song

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VibeFinder 1.0",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS — synthwave dark theme ───────────────────────────────────────
st.markdown("""
<style>
  /* ── Background & base text ── */
  .stApp { background-color: #0d0d1a; color: #e0e0f0; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10102a 0%, #1a0a2e 100%);
    border-right: 1px solid #3a1a5e;
  }

  /* ── Main heading ── */
  .vf-title {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: 0.04em;
    background: linear-gradient(90deg, #c850c0, #4158d0, #00e5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
  }
  .vf-subtitle {
    color: #8888aa;
    font-size: 0.95rem;
    margin-top: 0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  /* ── Song card ── */
  .song-card {
    background: linear-gradient(135deg, #12122a 0%, #1e0e3a 100%);
    border: 1px solid #3a1a5e;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
  }
  .song-card::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #c850c0, #4158d0);
    border-radius: 4px 0 0 4px;
  }
  .rank-badge {
    display: inline-block;
    font-size: 1.5rem;
    font-weight: 900;
    color: #4158d0;
    margin-right: 0.5rem;
    vertical-align: middle;
  }
  .song-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e8ff;
    display: inline;
  }
  .song-artist {
    color: #9988bb;
    font-size: 0.85rem;
    margin-top: 0.15rem;
  }

  /* ── Score bar ── */
  .score-bar-bg {
    background: #1a1a35;
    border-radius: 999px;
    height: 8px;
    margin: 0.55rem 0 0.45rem;
    overflow: hidden;
  }
  .score-bar-fill {
    height: 8px;
    border-radius: 999px;
    background: linear-gradient(90deg, #c850c0, #4158d0, #00e5ff);
    transition: width 0.4s ease;
  }

  /* ── Reason tags ── */
  .reason-tag {
    display: inline-block;
    background: rgba(65, 88, 208, 0.18);
    color: #a0b4ff;
    border: 1px solid rgba(65, 88, 208, 0.35);
    border-radius: 999px;
    padding: 0.15rem 0.6rem;
    font-size: 0.72rem;
    margin: 0.15rem 0.15rem 0 0;
  }

  /* ── Section divider ── */
  .neon-divider {
    border: none;
    border-top: 1px solid #2a1a4e;
    margin: 1.2rem 0;
  }

  /* ── Profile badge ── */
  .profile-badge {
    display: inline-block;
    background: linear-gradient(90deg, #c850c020, #4158d020);
    border: 1px solid #c850c055;
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
    color: #d0aaff;
    margin-bottom: 0.6rem;
  }

  /* ── Slider & select overrides ── */
  [data-testid="stSlider"] > div > div { background: #3a1a5e !important; }
  [data-testid="stSelectbox"] { color: #e0e0f0; }
  .stButton > button {
    background: linear-gradient(90deg, #c850c0, #4158d0) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")

songs = get_songs()
genres = sorted(set(s["genre"] for s in songs))
moods  = sorted(set(s["mood"]  for s in songs))

PRESETS = {
    "High-Energy Pop Fan": {"genre": "pop",        "mood": "happy",   "energy": 0.85, "likes_acoustic": False},
    "Chill Lofi Listener": {"genre": "lofi",       "mood": "chill",   "energy": 0.38, "likes_acoustic": True},
    "Intense Rock Head":   {"genre": "rock",       "mood": "intense", "energy": 0.90, "likes_acoustic": False},
    "Midnight EDM":        {"genre": "electronic", "mood": "moody",   "energy": 0.88, "likes_acoustic": False},
    "Acoustic Sunday":     {"genre": "acoustic",   "mood": "relaxed", "energy": 0.30, "likes_acoustic": True},
    "Custom":              None,
}

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Taste Profile")
    preset_key = st.selectbox("Preset", list(PRESETS.keys()), index=0)

    preset = PRESETS[preset_key]

    if preset:
        genre_val   = preset["genre"]
        mood_val    = preset["mood"]
        energy_val  = preset["energy"]
        acoustic    = preset["likes_acoustic"]
        genre_idx   = genres.index(genre_val) if genre_val in genres else 0
        mood_idx    = moods.index(mood_val)   if mood_val  in moods  else 0
    else:
        genre_idx, mood_idx, energy_val, acoustic = 0, 0, 0.6, False

    disabled = preset is not None

    st.markdown("<hr class='neon-divider'>", unsafe_allow_html=True)
    sel_genre  = st.selectbox("Favorite Genre", genres, index=genre_idx, disabled=disabled)
    sel_mood   = st.selectbox("Favorite Mood",  moods,  index=mood_idx,  disabled=disabled)
    sel_energy = st.slider("Target Energy", 0.0, 1.0, energy_val, 0.01, disabled=disabled)
    sel_acous  = st.checkbox("Prefers Acoustic", value=acoustic, disabled=disabled)

    st.markdown("<hr class='neon-divider'>", unsafe_allow_html=True)
    top_k = st.slider("# of Recommendations", 3, 10, 5)

# ─── Active prefs ─────────────────────────────────────────────────────────────
if preset:
    user_prefs = preset
else:
    user_prefs = {"genre": sel_genre, "mood": sel_mood, "energy": sel_energy, "likes_acoustic": sel_acous}

recs = recommend_songs(user_prefs, songs, k=top_k)
MAX_SCORE = 4.5

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("<p class='vf-title'>VibeFinder</p>", unsafe_allow_html=True)
st.markdown("<p class='vf-subtitle'>Content-Based Music Recommender · v1.0</p>", unsafe_allow_html=True)
st.markdown("<hr class='neon-divider'>", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="large")

# ─── Left: Recommendations ───────────────────────────────────────────────────
with col_left:
    badge_label = preset_key if preset else "Custom Profile"
    st.markdown(f"<div class='profile-badge'>🎧 {badge_label}</div>", unsafe_allow_html=True)
    st.markdown(f"**Top {top_k} Picks**")

    rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, (song, score, explanation) in enumerate(recs):
        pct = min(score / MAX_SCORE * 100, 100)
        reasons = explanation.split(", ")
        tags = "".join(f"<span class='reason-tag'>{r}</span>" for r in reasons)

        st.markdown(f"""
        <div class="song-card">
          <span class="rank-badge">{rank_emojis[i]}</span>
          <span class="song-title">{song['title']}</span>
          <div class="song-artist">by {song['artist']} &nbsp;·&nbsp; {song['genre']} &nbsp;·&nbsp; {song['mood']}</div>
          <div class="score-bar-bg">
            <div class="score-bar-fill" style="width:{pct:.1f}%"></div>
          </div>
          <small style="color:#7766aa">Score: <b style="color:#c0aaff">{score:.2f}</b> / 4.50</small><br/>
          {tags}
        </div>
        """, unsafe_allow_html=True)

# ─── Right: Radar chart ───────────────────────────────────────────────────────
with col_right:
    st.markdown("**Profile vs Top Pick**")

    top_song = recs[0][0]
    categories = ["Energy", "Valence", "Danceability", "Acousticness", "Tempo (norm)"]
    user_vals = [
        user_prefs["energy"],
        0.7,                             # valence not in prefs — neutral
        0.65,                            # danceability not in prefs — neutral
        1.0 if user_prefs["likes_acoustic"] else 0.15,
        0.5,                             # tempo not in prefs — neutral
    ]
    song_vals = [
        float(top_song["energy"]),
        float(top_song["valence"]),
        float(top_song["danceability"]),
        float(top_song["acousticness"]),
        (float(top_song["tempo_bpm"]) - 55) / (160 - 55),  # normalize 55–160 → 0–1
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=user_vals + [user_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Your Profile",
        line_color="#c850c0",
        fillcolor="rgba(200, 80, 192, 0.15)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=song_vals + [song_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=top_song["title"],
        line_color="#00e5ff",
        fillcolor="rgba(0, 229, 255, 0.10)",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#10102a",
            angularaxis=dict(color="#6655aa", gridcolor="#2a1a4e"),
            radialaxis=dict(visible=True, range=[0, 1], color="#6655aa", gridcolor="#2a1a4e"),
        ),
        showlegend=True,
        legend=dict(font=dict(color="#c0c0e0"), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="#0d0d1a",
        margin=dict(l=20, r=20, t=30, b=10),
        height=360,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Quick stats
    st.markdown("<hr class='neon-divider'>", unsafe_allow_html=True)
    st.markdown("**Catalog stats**")
    genre_counts = {}
    for s in songs:
        genre_counts[s["genre"]] = genre_counts.get(s["genre"], 0) + 1

    bar_fig = go.Figure(go.Bar(
        x=list(genre_counts.keys()),
        y=list(genre_counts.values()),
        marker_color="#4158d0",
        marker_line_color="#c850c0",
        marker_line_width=1,
    ))
    bar_fig.update_layout(
        paper_bgcolor="#0d0d1a",
        plot_bgcolor="#10102a",
        font=dict(color="#9988bb"),
        margin=dict(l=10, r=10, t=10, b=60),
        height=200,
        xaxis=dict(tickangle=-40, gridcolor="#1a1a35"),
        yaxis=dict(gridcolor="#1a1a35"),
    )
    st.plotly_chart(bar_fig, use_container_width=True)
