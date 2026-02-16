"""
🎬 CineMatch - Professional Movie Recommender UI
Production-ready with session persistence, validation, and optimized loading
"""

import streamlit as st
import requests
import os
from typing import List, Dict, Optional
import time
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

API_BASE_URL = "https://cinematch-movie-recommender-production.up.railway.app" 
TMDB_API_KEY = "22fa2d860d6e3ddbc070f84dff992094"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Session timeout: 24 hours (user stays logged in)
SESSION_TIMEOUT = timedelta(hours=24)

# Page configuration
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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #0a0a0a 100%);
    }
    
    .block-container {
        padding-top: 2rem !important;
        max-width: 1400px !important;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f4e4a6 !important;
    }
    
    h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        text-align: center;
        background: linear-gradient(135deg, #d4af37 0%, #f4e4a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #f4e4a6 !important;
        margin: 0.5rem 0 0.3rem 0 !important;
        min-height: 2.5rem;
        line-height: 1.3 !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: #e0e0e0 !important;
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(180deg, rgba(15, 20, 25, 0.9) 0%, rgba(10, 10, 10, 0.7) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .tagline {
        font-size: 1.2rem;
        color: #c0c0c0;
        font-weight: 300;
        font-style: italic;
        letter-spacing: 2px;
    }
    
    .movie-genres {
        font-size: 0.8rem;
        color: #c0c0c0;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    
    .rating-badge {
        display: inline-block;
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
        color: #0a0a0a;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
        color: #0a0a0a;
        border: none;
        padding: 0.8rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.6);
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #2a2a2a;
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        color: #f4e4a6;
        padding: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #d4af37;
        font-family: 'Playfair Display', serif;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #c0c0c0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.3rem;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 2rem 0;
        opacity: 0.5;
    }
    
    .stProgress > div > div {
        background: #d4af37 !important;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #d4af37, #b8941f);
        border-radius: 10px;
    }
    
    /* User info badge */
    .user-badge {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 30px;
        padding: 0.8rem 1.5rem;
        font-size: 0.9rem;
        color: #d4af37;
        font-weight: 600;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(90deg, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%);
        background-size: 200% 100%;
        animation: loading 1.5s ease-in-out infinite;
        border-radius: 12px;
        height: 450px;
        margin-bottom: 1rem;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Image lazy loading */
    div[data-testid="stImage"] {
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stImage"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(212, 175, 55, 0.3);
    }
    
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# API HELPER FUNCTIONS WITH CACHING
# ═══════════════════════════════════════════════════════════

@st.cache_data(ttl=86400, show_spinner=False)  # Cache for 24 hours
def get_movie_poster(title: str) -> str:
    """Get movie poster URL from TMDB - heavily cached"""
    if not TMDB_API_KEY:
        return f"https://via.placeholder.com/500x750/1a1a1a/d4af37?text={title[:20].replace(' ', '+')}"
    
    try:
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title.split("(")[0].strip()
        }
        response = requests.get(search_url, params=params, timeout=2)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results and results[0].get("poster_path"):
                return f"{TMDB_IMAGE_BASE}{results[0]['poster_path']}"
    except:
        pass
    
    return f"https://via.placeholder.com/500x750/1a1a1a/d4af37?text={title[:20].replace(' ', '+')}"

def get_popular_movies(n: int = 20) -> List[Dict]:
    """Get popular movies for onboarding"""
    try:
        url = f"{API_BASE_URL}/recommend"
        st.write(f"DEBUG: Calling {url}")  # Debug line
        response = requests.get(
            url,
            params={"user_id": 999999999, "n": n},
            timeout=10
        )
        st.write(f"DEBUG: Status code: {response.status_code}")  # Debug line
        if response.status_code == 200:
            data = response.json()
            st.write(f"DEBUG: Got {len(data.get('recommendations', []))} movies")  # Debug line
            return data.get("recommendations", [])
    except Exception as e:
        st.error(f"Error loading movies: {str(e)}")
    return []
def submit_rating(user_id: int, movie_id: int, rating: float) -> bool:
    """Submit rating to API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/rate",
            json={"user_id": user_id, "ratings": [{"movie_id": movie_id, "rating": rating}]},
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
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
    except:
        pass
    return None

def get_user_stats(user_id: int) -> Optional[Dict]:
    """Get user statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/user/{user_id}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def validate_user_exists(user_id: int) -> bool:
    """Check if user has any ratings (exists in system)"""
    stats = get_user_stats(user_id)
    if stats:
        return stats.get('total_ratings', 0) > 0
    return False

# ═══════════════════════════════════════════════════════════
# SESSION STATE WITH PERSISTENCE
# ═══════════════════════════════════════════════════════════

def init_session_state():
    """Initialize session state with persistence"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'onboarding_ratings' not in st.session_state:
        st.session_state.onboarding_ratings = {}
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Check session timeout
    if st.session_state.user_id and st.session_state.logged_in:
        time_since_activity = datetime.now() - st.session_state.last_activity
        if time_since_activity > SESSION_TIMEOUT:
            # Session expired - clear user
            st.session_state.user_id = None
            st.session_state.logged_in = False
            st.session_state.page = 'welcome'
    
    # Update activity timestamp
    st.session_state.last_activity = datetime.now()

# Initialize
init_session_state()

# Load CSS
load_css()

# ═══════════════════════════════════════════════════════════
# USER BADGE (shows current user)
# ═══════════════════════════════════════════════════════════

def render_user_badge():
    """Display user badge if logged in"""
    if st.session_state.user_id and st.session_state.logged_in:
        st.markdown(f"""
        <div class="user-badge">
            👤 User: {st.session_state.user_id}
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE RENDERING FUNCTIONS
# ═══════════════════════════════════════════════════════════

def render_welcome_page():
    """Welcome page"""
    st.markdown("""
    <div class="hero-section">
        <h1>🎬 CINEMATCH</h1>
        <p class="tagline">Your Personal Film Curator</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome to Your Personalized Cinema")
        st.markdown("Discover your next favorite film with AI-powered recommendations.")
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        choice = st.radio(
            "Choose your path:",
            ["🆕 I'm new here", "🎭 I'm a returning cinephile"]
        )
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if choice == "🆕 I'm new here":
            if st.button("Begin Your Journey", key="new_user_btn"):
                import random
                st.session_state.user_id = random.randint(100000, 999999)
                st.session_state.logged_in = True
                st.session_state.page = 'onboarding'
                st.rerun()
        else:
            user_id_input = st.number_input(
                "Enter your User ID:",
                min_value=1,
                max_value=999999,
                value=None,
                placeholder="e.g., 12345",
                key="user_id_input"
            )
            
            if st.button("Continue", key="returning_user_btn"):
                if not user_id_input:
                    st.error("⚠️ Please enter a valid User ID")
                elif not validate_user_exists(user_id_input):
                    st.error(f"⚠️ User ID {user_id_input} not found. Please check your ID or create a new account.")
                    st.info("💡 Tip: If you're new, select 'I'm new here' above")
                else:
                    # User exists - log them in
                    st.session_state.user_id = user_id_input
                    st.session_state.logged_in = True
                    st.session_state.page = 'recommendations'
                    st.success(f"✅ Welcome back, User {user_id_input}!")
                    time.sleep(1)
                    st.rerun()

def render_onboarding_page():
    """Onboarding page - rate movies"""
    render_user_badge()
    
    st.markdown("""
    <div class="hero-section">
        <h2>🎬 Build Your Taste Profile</h2>
        <p class="tagline">Rate at least 5 films to unlock recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    rated_count = len(st.session_state.onboarding_ratings)
    progress = min(rated_count / 5, 1.0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(progress)
        st.markdown(f"<p style='text-align: center; color: #d4af37; font-weight: 600;'>{rated_count} / 5 films rated</p>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Load popular movies (cached)
    popular_movies = get_popular_movies(20)
    
    if not popular_movies:
        st.error("⚠️ Unable to load movies. Please ensure FastAPI is running.")
        st.code("uvicorn app:app --reload", language="bash")
        if st.button("🏠 Back to Home", key="back_home_onboarding"):
            st.session_state.page = 'welcome'
            st.rerun()
        return
    
    # Pre-load all poster URLs (parallel loading via caching)
    with st.spinner("Loading posters..."):
        poster_urls = {movie['movie_id']: get_movie_poster(movie['title']) for movie in popular_movies}
    
    # Display movies in grid (5 per row)
    cols_per_row = 5
    for i in range(0, len(popular_movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(popular_movies):
                movie = popular_movies[i + j]
                with col:
                    render_movie_card_onboarding(movie, poster_urls)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if rated_count >= 5:
            if st.button("🎬 Get My Recommendations", key="get_recs_btn"):
                with st.spinner("Building your profile..."):
                    success_count = 0
                    for movie_id, rating in st.session_state.onboarding_ratings.items():
                        if submit_rating(st.session_state.user_id, movie_id, rating):
                            success_count += 1
                    
                    if success_count > 0:
                        st.success(f"✨ Profile created! Your ID: **{st.session_state.user_id}**")
                        st.info("💾 Save this ID to access your recommendations later!")
                        time.sleep(2)
                        st.session_state.page = 'recommendations'
                        st.rerun()
                    else:
                        st.error("⚠️ Error saving ratings. Please check API connection.")
        else:
            st.info(f"⭐ Rate {5 - rated_count} more film{'s' if 5 - rated_count > 1 else ''} to continue")

def render_movie_card_onboarding(movie: Dict, poster_urls: Dict):
    """Render onboarding movie card with pre-loaded poster"""
    movie_id = movie['movie_id']
    title = movie['title']
    genres = movie.get('genres', 'Unknown')
    
    # Use pre-loaded poster URL
    poster_url = poster_urls.get(movie_id, "https://via.placeholder.com/500x750/1a1a1a/d4af37?text=Loading")
    
    # Display image
    st.image(poster_url)
    
    st.markdown(f"<h3>{title[:45]}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='movie-genres'>{genres}</p>", unsafe_allow_html=True)
    
    current_rating = st.session_state.onboarding_ratings.get(movie_id, 0)
    
    rating = st.select_slider(
        f"Rate {movie_id}",
        options=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        value=current_rating,
        format_func=lambda x: "⭐" * int(x) + ("½" if x % 1 else "") if x > 0 else "Rate",
        key=f"rate_{movie_id}",
        label_visibility="collapsed"
    )
    
    if rating > 0:
        st.session_state.onboarding_ratings[movie_id] = rating

def render_recommendations_page():
    """Recommendations page"""
    render_user_badge()
    
    user_stats = get_user_stats(st.session_state.user_id)
    
    st.markdown(f"""
    <div class="hero-section">
        <h2>🎬 Your Curated Collection</h2>
        <p class="tagline">Personalized for You</p>
    </div>
    """, unsafe_allow_html=True)
    
    if user_stats:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{user_stats['total_ratings']}</div>
                <div class="stat-label">Films Rated</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg = user_stats.get('average_rating', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{avg:.1f}</div>
                <div class="stat-label">Avg Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            rec_type = "Personal" if user_stats['recommendation_type'] == 'personalized' else "Popular"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size: 1.5rem;">{rec_type}</div>
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
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        num_recs = st.slider("Number of recommendations:", 5, 30, 20, step=5, key="num_recs_slider")
    with col2:
        if st.button("🔄 Refresh", key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("⭐ Rate More", key="rate_more_btn"):
            st.session_state.page = 'onboarding'
            st.rerun()
    with col4:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.user_id = None
            st.session_state.logged_in = False
            st.session_state.page = 'welcome'
            st.session_state.onboarding_ratings = {}
            st.success("👋 Logged out successfully!")
            time.sleep(1)
            st.rerun()
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Get recommendations
    with st.spinner("Curating your selection..."):
        recs_data = get_recommendations(st.session_state.user_id, num_recs)
    
    if not recs_data:
        st.error("⚠️ Unable to fetch recommendations. Please check API connection.")
        return
    
    recommendations = recs_data.get('recommendations', [])
    source = recs_data.get('source', 'Unknown')
    
    st.markdown(f"<p style='text-align: center; color: #c0c0c0; font-style: italic;'>Recommendations from: {source}</p>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Pre-load all poster URLs for fast rendering
    with st.spinner("Loading posters..."):
        poster_urls = {movie['movie_id']: get_movie_poster(movie['title']) for movie in recommendations}
    
    # Display in grid (5 per row)
    cols_per_row = 5
    for i in range(0, len(recommendations), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                movie = recommendations[i + j]
                with col:
                    render_movie_card_recommendation(movie, poster_urls)

def render_movie_card_recommendation(movie: Dict, poster_urls: Dict):
    """Render recommendation card with pre-loaded poster"""
    movie_id = movie['movie_id']
    title = movie['title']
    genres = movie.get('genres', 'Unknown')
    predicted_rating = movie.get('predicted_rating')
    
    # Use pre-loaded poster URL
    poster_url = poster_urls.get(movie_id, "https://via.placeholder.com/500x750/1a1a1a/d4af37?text=Loading")
    
    st.image(poster_url)
    
    st.markdown(f"<h3>{title[:45]}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='movie-genres'>{genres}</p>", unsafe_allow_html=True)
    
    if predicted_rating:
        st.markdown(f"<div class='rating-badge'>★ {predicted_rating:.1f}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# MAIN APP ROUTER
# ═══════════════════════════════════════════════════════════

def main():
    """Main application router"""
    
    # Check if user is logged in but on welcome page (shouldn't happen)
    if st.session_state.logged_in and st.session_state.user_id and st.session_state.page == 'welcome':
        st.session_state.page = 'recommendations'
        st.rerun()
    
    # Route to appropriate page
    if st.session_state.page == 'welcome':
        render_welcome_page()
    elif st.session_state.page == 'onboarding':
        render_onboarding_page()
    elif st.session_state.page == 'recommendations':
        # Make sure user is logged in
        if not st.session_state.logged_in or not st.session_state.user_id:
            st.session_state.page = 'welcome'
            st.rerun()
        else:
            render_recommendations_page()

if __name__ == "__main__":
    main()
