"""
🎬 Movie Recommender - Cinematic UI
Professional-grade Streamlit interface with noir elegance
"""

import streamlit as st
import requests
import os
from typing import List, Dict, Optional
import time

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")  # Get from https://www.themoviedb.org/settings/api
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Page config with custom theme
st.set_page_config(
    page_title="CineMatch | Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════
# CUSTOM CSS - CINEMATIC NOIR ELEGANCE
# ═══════════════════════════════════════════════════════════

def load_css():
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════════════════════
       GLOBAL THEME - Cinematic Noir
       ═══════════════════════════════════════════════════════════ */
    
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        --noir-black: #0a0a0a;
        --noir-charcoal: #1a1a1a;
        --noir-slate: #2a2a2a;
        --gold-accent: #d4af37;
        --gold-light: #f4e4a6;
        --midnight-blue: #0f1419;
        --silver: #c0c0c0;
        --red-accent: #8b0000;
    }
    
    /* Remove Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, var(--midnight-blue) 0%, var(--noir-black) 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       TYPOGRAPHY - Playfair Display + Inter
       ═══════════════════════════════════════════════════════════ */
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--gold-light) !important;
        letter-spacing: 0.5px;
    }
    
    h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, var(--gold-accent) 0%, var(--gold-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
    }
    
    h2 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: var(--silver) !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: #e0e0e0 !important;
        line-height: 1.6;
    }
    
    /* ═══════════════════════════════════════════════════════════
       HERO SECTION
       ═══════════════════════════════════════════════════════════ */
    
    .hero-section {
        text-align: center;
        padding: 3rem 2rem 4rem 2rem;
        background: linear-gradient(180deg, rgba(15, 20, 25, 0.9) 0%, rgba(10, 10, 10, 0.7) 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-accent), transparent);
    }
    
    .tagline {
        font-size: 1.2rem;
        color: var(--silver);
        font-weight: 300;
        margin-top: 1rem;
        font-style: italic;
        letter-spacing: 2px;
    }
    
    /* ═══════════════════════════════════════════════════════════
       MOVIE CARDS - Premium Design
       ═══════════════════════════════════════════════════════════ */
    
    .movie-card {
        background: linear-gradient(145deg, var(--noir-charcoal) 0%, var(--noir-slate) 100%);
        border-radius: 16px;
        padding: 0;
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(212, 175, 55, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        position: relative;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: var(--gold-accent);
        box-shadow: 0 20px 60px rgba(212, 175, 55, 0.3),
                    0 0 40px rgba(212, 175, 55, 0.1);
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, transparent 0%, rgba(212, 175, 55, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .movie-card:hover::before {
        opacity: 1;
    }
    
    .movie-poster {
        width: 100%;
        height: 450px;
        object-fit: cover;
        border-radius: 16px 16px 0 0;
        transition: all 0.4s ease;
    }
    
    .movie-card:hover .movie-poster {
        filter: brightness(1.1) contrast(1.05);
    }
    
    .movie-info {
        padding: 1.5rem;
        background: linear-gradient(180deg, var(--noir-slate) 0%, var(--noir-charcoal) 100%);
    }
    
    .movie-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--gold-light) !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.3 !important;
        min-height: 2.6rem;
    }
    
    .movie-genres {
        font-size: 0.85rem;
        color: var(--silver);
        font-weight: 400;
        opacity: 0.8;
        margin-bottom: 1rem;
    }
    
    .rating-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--gold-accent) 0%, #b8941f 100%);
        color: var(--noir-black);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }
    
    /* ═══════════════════════════════════════════════════════════
       BUTTONS - Luxury Style
       ═══════════════════════════════════════════════════════════ */
    
    .stButton > button {
        background: linear-gradient(135deg, var(--gold-accent) 0%, #b8941f 100%);
        color: var(--noir-black);
        border: none;
        padding: 0.8rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.6);
        background: linear-gradient(135deg, #f4e4a6 0%, var(--gold-accent) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ═══════════════════════════════════════════════════════════
       INPUT FIELDS
       ═══════════════════════════════════════════════════════════ */
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--noir-slate);
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        color: var(--gold-light);
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--gold-accent);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        outline: none;
    }
    
    /* ═══════════════════════════════════════════════════════════
       RATING STARS
       ═══════════════════════════════════════════════════════════ */
    
    .rating-container {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin: 1rem 0;
    }
    
    .star-btn {
        background: none;
        border: none;
        font-size: 2rem;
        cursor: pointer;
        transition: all 0.2s ease;
        filter: drop-shadow(0 0 5px rgba(212, 175, 55, 0.3));
    }
    
    .star-btn:hover {
        transform: scale(1.2);
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.6));
    }
    
    /* ═══════════════════════════════════════════════════════════
       STATS CARDS
       ═══════════════════════════════════════════════════════════ */
    
    .stat-card {
        background: linear-gradient(135deg, var(--noir-charcoal) 0%, var(--noir-slate) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: var(--gold-accent);
        box-shadow: 0 12px 36px rgba(212, 175, 55, 0.2);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: var(--gold-accent);
        font-family: 'Playfair Display', serif;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--silver);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* ═══════════════════════════════════════════════════════════
       LOADING SPINNER
       ═══════════════════════════════════════════════════════════ */
    
    .stSpinner > div {
        border-color: var(--gold-accent) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       SUCCESS/ERROR MESSAGES
       ═══════════════════════════════════════════════════════════ */
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 139, 34, 0.2) 0%, rgba(34, 139, 34, 0.1) 100%);
        border: 1px solid rgba(34, 139, 34, 0.5);
        border-radius: 12px;
        color: #90EE90 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.2) 0%, rgba(139, 0, 0, 0.1) 100%);
        border: 1px solid rgba(139, 0, 0, 0.5);
        border-radius: 12px;
        color: #FF6B6B !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       DIVIDER
       ═══════════════════════════════════════════════════════════ */
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-accent), transparent);
        margin: 3rem 0;
        opacity: 0.5;
    }
    
    /* ═══════════════════════════════════════════════════════════
       SCROLLBAR
       ═══════════════════════════════════════════════════════════ */
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--noir-black);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--gold-accent), #b8941f);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gold-light);
    }
    
    /* ═══════════════════════════════════════════════════════════
       ANIMATIONS
       ═══════════════════════════════════════════════════════════ */
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* ═══════════════════════════════════════════════════════════
       SELECT BOX
       ═══════════════════════════════════════════════════════════ */
    
    .stSelectbox > div > div {
        background: var(--noir-slate);
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        color: var(--gold-light);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--gold-accent);
    }
    
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# API HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_movie_poster(title: str, tmdb_id: Optional[int] = None) -> str:
    """Get movie poster from TMDB or return placeholder"""
    if not TMDB_API_KEY:
        return f"https://via.placeholder.com/500x750/1a1a1a/d4af37?text={title[:20]}"
    
    try:
        # Search for movie
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title.split("(")[0].strip()  # Remove year
        }
        response = requests.get(search_url, params=params, timeout=3)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                poster_path = results[0].get("poster_path")
                if poster_path:
                    return f"{TMDB_IMAGE_BASE}{poster_path}"
    except:
        pass
    
    return f"https://via.placeholder.com/500x750/1a1a1a/d4af37?text={title[:20]}"

def submit_rating(user_id: int, movie_id: int, rating: float) -> bool:
    """Submit a rating to the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/rate",
            json={
                "user_id": user_id,
                "ratings": [{"movie_id": movie_id, "rating": rating}]
            },
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error submitting rating: {e}")
        return False

def get_recommendations(user_id: int, n: int = 20) -> Optional[Dict]:
    """Get recommendations from API"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/recommend",
            params={"user_id": user_id, "n": n},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
    return None

def get_user_stats(user_id: int) -> Optional[Dict]:
    """Get user statistics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/user/{user_id}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_popular_movies(n: int = 20) -> List[Dict]:
    """Get popular movies for onboarding"""
    try:
        # Use a temporary user ID to get popular movies
        response = requests.get(
            f"{API_BASE_URL}/recommend",
            params={"user_id": 999999999, "n": n},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("recommendations", [])
    except:
        pass
    return []

# ═══════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'onboarding_ratings' not in st.session_state:
    st.session_state.onboarding_ratings = {}

# ═══════════════════════════════════════════════════════════
# LOAD CUSTOM CSS
# ═══════════════════════════════════════════════════════════

load_css()

# ═══════════════════════════════════════════════════════════
# PAGE ROUTING
# ═══════════════════════════════════════════════════════════

def render_welcome_page():
    """Welcome/Landing Page"""
    
    st.markdown("""
    <div class="hero-section fade-in">
        <h1>🎬 CINEMATCH</h1>
        <p class="tagline">Your Personal Film Curator</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome to Your Personalized Cinema")
        st.markdown("Discover your next favorite film with AI-powered recommendations tailored to your taste.")
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Choice buttons
        choice = st.radio(
            "Choose your path:",
            ["🆕 I'm new here", "🎭 I'm a returning cinephile"],
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        if choice == "🆕 I'm new here":
            if st.button("Begin Your Journey", use_container_width=True):
                # Generate new user ID
                import random
                st.session_state.user_id = random.randint(100000, 999999)
                st.session_state.page = 'onboarding'
                st.rerun()
        else:
            user_id_input = st.number_input(
                "Enter your User ID:",
                min_value=1,
                max_value=999999,
                value=None,
                placeholder="e.g., 12345"
            )
            
            if st.button("Continue", use_container_width=True):
                if user_id_input:
                    st.session_state.user_id = user_id_input
                    st.session_state.page = 'recommendations'
                    st.rerun()
                else:
                    st.error("Please enter a valid User ID")

def render_onboarding_page():
    """Onboarding - Rate movies to build profile"""
    
    st.markdown("""
    <div class="hero-section fade-in">
        <h2>🎬 Build Your Taste Profile</h2>
        <p class="tagline">Rate at least 5 films to unlock personalized recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    rated_count = len(st.session_state.onboarding_ratings)
    progress = min(rated_count / 5, 1.0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(progress)
        st.markdown(f"<p style='text-align: center; color: var(--gold-accent);'>{rated_count} / 5 films rated</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Get popular movies
    with st.spinner("Loading film selection..."):
        popular_movies = get_popular_movies(20)
    
    if not popular_movies:
        st.error("Unable to load movies. Please check your API connection.")
        return
    
    # Display movies in grid
    cols_per_row = 4
    for i in range(0, len(popular_movies), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(popular_movies):
                movie = popular_movies[i + j]
                with col:
                    render_movie_card_onboarding(movie)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if rated_count >= 5:
            if st.button("🎬 Get My Recommendations", use_container_width=True):
                # Submit all ratings
                with st.spinner("Building your profile..."):
                    success = True
                    for movie_id, rating in st.session_state.onboarding_ratings.items():
                        if not submit_rating(st.session_state.user_id, movie_id, rating):
                            success = False
                    
                    if success:
                        st.success(f"Profile created! Your ID: {st.session_state.user_id}")
                        time.sleep(1)
                        st.session_state.page = 'recommendations'
                        st.rerun()
                    else:
                        st.error("Error saving ratings. Please try again.")
        else:
            st.info(f"Rate {5 - rated_count} more film{'s' if 5 - rated_count > 1 else ''} to continue")

def render_movie_card_onboarding(movie: Dict):
    """Render a movie card for onboarding"""
    movie_id = movie['movie_id']
    title = movie['title']
    genres = movie.get('genres', 'Unknown')
    
    poster_url = get_movie_poster(title)
    
    st.markdown(f"""
    <div class="movie-card">
        <img src="{poster_url}" class="movie-poster" alt="{title}">
        <div class="movie-info">
            <div class="movie-title">{title[:50]}</div>
            <div class="movie-genres">{genres}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Star rating
    current_rating = st.session_state.onboarding_ratings.get(movie_id, 0)
    
    rating = st.select_slider(
        f"Rate {movie_id}",
        options=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        value=current_rating,
        format_func=lambda x: "⭐" * int(x) + ("½" if x % 1 else ""),
        key=f"rate_{movie_id}",
        label_visibility="collapsed"
    )
    
    if rating > 0:
        st.session_state.onboarding_ratings[movie_id] = rating

def render_recommendations_page():
    """Main recommendations page"""
    
    # Get user stats
    user_stats = get_user_stats(st.session_state.user_id)
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="hero-section fade-in">
            <h2>🎬 Your Curated Collection</h2>
            <p class="tagline">User ID: {st.session_state.user_id}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats cards
    if user_stats:
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{user_stats['total_ratings']}</div>
                <div class="stat-label">Films Rated</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_rating = user_stats.get('average_rating', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{avg_rating:.1f}</div>
                <div class="stat-label">Avg Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            rec_type = "Personalized" if user_stats['recommendation_type'] == 'personalized' else "Popular"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{rec_type}</div>
                <div class="stat-label">Mode</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            in_training = "✓" if user_stats['in_training_data'] else "✗"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{in_training}</div>
                <div class="stat-label">In Training</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        num_recs = st.slider("Number of recommendations:", 5, 30, 20, step=5)
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.user_id = None
            st.session_state.onboarding_ratings = {}
            st.rerun()
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Get recommendations
    with st.spinner("Curating your personalized selection..."):
        recs_data = get_recommendations(st.session_state.user_id, num_recs)
    
    if not recs_data:
        st.error("Unable to fetch recommendations. Please check your API connection.")
        return
    
    recommendations = recs_data.get('recommendations', [])
    source = recs_data.get('source', 'Unknown')
    
    st.markdown(f"<p style='text-align: center; color: var(--silver); font-style: italic;'>Recommendations from: {source}</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Display recommendations in grid
    cols_per_row = 5
    for i in range(0, len(recommendations), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                movie = recommendations[i + j]
                with col:
                    render_movie_card_recommendation(movie)

def render_movie_card_recommendation(movie: Dict):
    """Render a movie card for recommendations"""
    title = movie['title']
    genres = movie.get('genres', 'Unknown')
    predicted_rating = movie.get('predicted_rating')
    
    poster_url = get_movie_poster(title)
    
    rating_html = ""
    if predicted_rating:
        rating_html = f'<div class="rating-badge">★ {predicted_rating:.1f}</div>'
    
    st.markdown(f"""
    <div class="movie-card">
        <img src="{poster_url}" class="movie-poster" alt="{title}">
        <div class="movie-info">
            <div class="movie-title">{title[:50]}</div>
            <div class="movie-genres">{genres}</div>
            {rating_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# MAIN APP ROUTING
# ═══════════════════════════════════════════════════════════

def main():
    """Main application router"""
    
    if st.session_state.page == 'welcome':
        render_welcome_page()
    elif st.session_state.page == 'onboarding':
        render_onboarding_page()
    elif st.session_state.page == 'recommendations':
        render_recommendations_page()

if __name__ == "__main__":
    main()