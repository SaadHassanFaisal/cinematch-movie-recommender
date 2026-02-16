from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import pandas as pd
import numpy as np
import joblib
import os
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI(
    title="Movie Recommender API",
    description="Personalized movie recommendation system with collaborative filtering",
    version="1.0.0"
)

# Add CORS middleware to allow Streamlit to connect
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────────────────────────
# Configuration & Path Setup
# ────────────────────────────────────────────────
# Use environment variable or fallback to default
# ════════════════════════════════════════════════
# CONFIGURATION & PATH SETUP
# ════════════════════════════════════════════════
# Use environment variable or fallback to current directory
ROOT_DIR = os.getenv("MODEL_PATH", os.path.dirname(os.path.abspath(__file__)))

# NOTE: Skip validation in Docker - files are in same directory as app.py
# ────────────────────────────────────────────────
# Load Data & Model Artifacts
# ────────────────────────────────────────────────
print("Loading model artifacts...")

try:
    # Load ratings for popularity fallback
    ratings_path = os.path.join(ROOT_DIR, "ratings_processed.csv")
    ratings = pd.read_csv(ratings_path)
    print(f"✓ Loaded {len(ratings):,} ratings")
    
    # Load FunkSVD model
    model_path = os.path.join(ROOT_DIR, "funksvd_model.npz")
    loaded = np.load(model_path)
    
    # Reconstruct model object
    class FunkSVD:
        def __init__(self):
            self.user_factors = loaded['user_factors']
            self.item_factors = loaded['item_factors']
            self.user_bias = loaded['user_bias']
            self.item_bias = loaded['item_bias']
            self.global_mean = float(loaded['global_mean'])
            
        def predict_all(self, user_idx):
            """Vectorized prediction for all items for a given user"""
            if user_idx >= len(self.user_bias):
                raise ValueError(f"User index {user_idx} out of bounds")
            
            base = self.global_mean + self.user_bias[user_idx] + self.item_bias
            scores = base + np.dot(self.user_factors[user_idx], self.item_factors.T)
            return scores
    
    model = FunkSVD()
    print(f"✓ Loaded FunkSVD model (users={len(model.user_factors)}, items={len(model.item_factors)})")
    
    # Load ID mappings
    mappings_path = os.path.join(ROOT_DIR, "id_mappings.pkl")
    mappings = joblib.load(mappings_path)
    user_map = mappings['user_map']  # {original_user_id: user_idx}
    movie_map = mappings['movie_map']  # {original_movie_id: movie_idx}
    
    # Create reverse mappings (CRITICAL FIX)
    idx_to_movie_id = {idx: mid for mid, idx in movie_map.items()}
    idx_to_user_id = {idx: uid for uid, idx in user_map.items()}
    
    print(f"✓ Loaded mappings (users={len(user_map)}, movies={len(movie_map)})")
    
    # Load movies metadata
    movies_path = os.path.join(ROOT_DIR, "movies_metadata.csv")
    movies = pd.read_csv(movies_path)
    
    # Ensure movie_id is int for consistent filtering
    movies['movie_id'] = movies['movie_id'].astype(int)
    
    print(f"✓ Loaded {len(movies):,} movies metadata")
    
except FileNotFoundError as e:
    raise RuntimeError(f"Required file not found: {e}")
except Exception as e:
    raise RuntimeError(f"Error loading model artifacts: {e}")

# ────────────────────────────────────────────────
# SQLite Database Setup
# ────────────────────────────────────────────────
db_dir = os.path.join(ROOT_DIR, "data")
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "user_ratings.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = declarative_base()

class UserRating(Base):
    """User rating storage with composite primary key"""
    __tablename__ = "user_ratings"
    
    # FIXED: Remove individual primary_key=True when using composite key
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    
    # Composite primary key
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
    
    # Define composite primary key properly
    from sqlalchemy import PrimaryKeyConstraint
    __table_args__ = (PrimaryKeyConstraint('user_id', 'movie_id'),)

# Create tables
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

print(f"✓ Database initialized at {db_path}")

# ────────────────────────────────────────────────
# Database dependency
# ────────────────────────────────────────────────
def get_db():
    """FastAPI dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ────────────────────────────────────────────────
# Pydantic Models (Request/Response schemas)
# ────────────────────────────────────────────────
class Rating(BaseModel):
    movie_id: int = Field(..., description="Movie ID", gt=0)
    rating: float = Field(..., description="Rating value", ge=0.5, le=5.0)
    
    @validator('rating')
    def validate_rating(cls, v):
        """Ensure rating is in valid range and increment of 0.5"""
        if v < 0.5 or v > 5.0:
            raise ValueError('Rating must be between 0.5 and 5.0')
        # Allow ratings in 0.5 increments
        if (v * 2) % 1 != 0:
            raise ValueError('Rating must be in 0.5 increments (e.g., 3.5, 4.0)')
        return v

class RateRequest(BaseModel):
    user_id: int = Field(..., description="User ID", gt=0)
    ratings: List[Rating] = Field(..., description="List of movie ratings", min_items=1)
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 12345,
                "ratings": [
                    {"movie_id": 1, "rating": 4.5},
                    {"movie_id": 2, "rating": 3.0},
                ]
            }
        }

class Recommendation(BaseModel):
    movie_id: int
    title: str
    genres: str
    predicted_rating: Optional[float] = None

class RecommendResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]
    source: str
    count: int

# ────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────
def get_user_rated_movies(db: Session, user_id: int) -> set:
    """Get set of movie IDs the user has already rated"""
    user_ratings = db.query(UserRating.movie_id).filter_by(user_id=user_id).all()
    return {r.movie_id for r in user_ratings}

def get_popularity_recommendations(n: int, exclude_movie_ids: set = None) -> List[dict]:
    """
    Get top-N popular movies based on rating count and mean rating
    
    Args:
        n: Number of recommendations
        exclude_movie_ids: Set of movie IDs to exclude (already rated)
    
    Returns:
        List of movie dictionaries
    """
    # Calculate movie statistics
    movie_stats = ratings.groupby('movie_id').agg(
        mean_rating=('rating', 'mean'),
        count=('rating', 'count')
    ).reset_index()
    
    # Filter out movies with too few ratings (noise)
    movie_stats = movie_stats[movie_stats['count'] >= 50]
    
    # Exclude already rated movies
    if exclude_movie_ids:
        movie_stats = movie_stats[~movie_stats['movie_id'].isin(exclude_movie_ids)]
    
    # Sort by mean rating (weighted by count)
    movie_stats['weighted_score'] = (
        movie_stats['mean_rating'] * np.log1p(movie_stats['count'])
    )
    movie_stats = movie_stats.sort_values('weighted_score', ascending=False)
    
    # Get top N movie IDs
    top_ids = movie_stats.head(n)['movie_id'].tolist()
    
    # Fetch movie details
    recs = movies[movies['movie_id'].isin(top_ids)][
        ['movie_id', 'title', 'genres']
    ].to_dict('records')
    
    return recs

def get_personalized_recommendations(
    user_id: int, 
    n: int, 
    exclude_movie_ids: set = None
) -> tuple[List[dict], str]:
    """
    Get personalized recommendations using FunkSVD
    
    Returns:
        (recommendations, source_description)
    """
    # Check if user in training data
    if user_id not in user_map:
        return get_popularity_recommendations(n, exclude_movie_ids), "popularity (user not in training data)"
    
    try:
        u_idx = user_map[user_id]
        
        # Get predictions for all movies (FAST - vectorized)
        scores = model.predict_all(u_idx)
        
        # CRITICAL FIX: Use proper reverse mapping
        # Get top N indices (excluding already rated)
        if exclude_movie_ids:
            # Zero out scores for already rated movies
            for movie_id in exclude_movie_ids:
                if movie_id in movie_map:
                    m_idx = movie_map[movie_id]
                    scores[m_idx] = -np.inf
        
        # Get top N movie indices
        top_indices = np.argsort(-scores)[:n * 2]  # Get extra in case some don't have metadata
        
        # Convert indices to movie IDs using reverse mapping
        top_movie_ids = []
        predicted_ratings = []
        
        for idx in top_indices:
            if idx in idx_to_movie_id:
                movie_id = idx_to_movie_id[idx]
                top_movie_ids.append(movie_id)
                predicted_ratings.append(scores[idx])
                
                if len(top_movie_ids) >= n:
                    break
        
        # Fetch movie details
        recs = movies[movies['movie_id'].isin(top_movie_ids)][
            ['movie_id', 'title', 'genres']
        ].to_dict('records')
        
        # Add predicted ratings
        rating_map = dict(zip(top_movie_ids, predicted_ratings))
        for rec in recs:
            rec['predicted_rating'] = round(rating_map.get(rec['movie_id'], 0), 2)
        
        # Sort by predicted rating (in case order was lost during merge)
        recs = sorted(recs, key=lambda x: x.get('predicted_rating', 0), reverse=True)[:n]
        
        return recs, "FunkSVD (personalized)"
        
    except Exception as e:
        print(f"Error in personalized recommendations: {e}")
        return get_popularity_recommendations(n, exclude_movie_ids), f"popularity (error: {str(e)})"

# ────────────────────────────────────────────────
# API Endpoints
# ────────────────────────────────────────────────

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Movie Recommender API",
        "version": "1.0.0",
        "model": "FunkSVD",
        "endpoints": ["/rate", "/recommend"]
    }

@app.post("/rate", response_model=dict)
def submit_ratings(request: RateRequest, db: Session = Depends(get_db)):
    """
    Submit user ratings for movies
    
    - **user_id**: User identifier (integer)
    - **ratings**: List of {movie_id, rating} pairs
    
    Ratings are stored in SQLite database and can be updated.
    """
    try:
        # Validate that movies exist in the system
        valid_movie_ids = set(movies['movie_id'].unique())
        invalid_movies = [
            r.movie_id for r in request.ratings 
            if r.movie_id not in valid_movie_ids
        ]
        
        if invalid_movies:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid movie IDs: {invalid_movies}. These movies don't exist in the system."
            )
        
        # Upsert ratings
        for r in request.ratings:
            existing = db.query(UserRating).filter_by(
                user_id=request.user_id,
                movie_id=r.movie_id
            ).first()
            
            if existing:
                existing.rating = r.rating
            else:
                new_rating = UserRating(
                    user_id=request.user_id,
                    movie_id=r.movie_id,
                    rating=r.rating
                )
                db.add(new_rating)
        
        db.commit()
        
        # Get updated count
        total_ratings = db.query(UserRating).filter_by(user_id=request.user_id).count()
        
        return {
            "status": "success",
            "message": f"Successfully submitted {len(request.ratings)} rating(s)",
            "user_id": request.user_id,
            "total_user_ratings": total_ratings
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/recommend", response_model=RecommendResponse)
def get_recommendations(
    user_id: int,
    n: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get personalized movie recommendations
    
    - **user_id**: User identifier
    - **n**: Number of recommendations (default: 10, max: 50)
    
    Returns personalized recommendations using FunkSVD if user has enough ratings,
    otherwise returns popular movies (cold start).
    """
    # Validate parameters
    if n < 1 or n > 50:
        raise HTTPException(status_code=400, detail="n must be between 1 and 50")
    
    try:
        # Get user's rated movies
        rated_movies = get_user_rated_movies(db, user_id)
        user_rating_count = len(rated_movies)
        
        # Decide recommendation strategy
        # Cold start threshold: user needs at least 5 ratings for personalization
        COLD_START_THRESHOLD = 5
        
        if user_rating_count < COLD_START_THRESHOLD:
            # Cold start: use popularity
            recs = get_popularity_recommendations(n, rated_movies)
            source = f"popularity (cold start: {user_rating_count} ratings)"
        else:
            # Personalized recommendations
            recs, source = get_personalized_recommendations(user_id, n, rated_movies)
        
        # Handle edge case: no recommendations found
        if not recs:
            recs = get_popularity_recommendations(n, rated_movies)
            source = "popularity (fallback)"
        
        return RecommendResponse(
            user_id=user_id,
            recommendations=recs[:n],  # Ensure we return exactly n
            source=source,
            count=len(recs[:n])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.get("/user/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Get statistics for a specific user"""
    user_ratings = db.query(UserRating).filter_by(user_id=user_id).all()
    
    if not user_ratings:
        return {
            "user_id": user_id,
            "total_ratings": 0,
            "in_training_data": user_id in user_map,
            "recommendation_type": "cold_start"
        }
    
    ratings_list = [r.rating for r in user_ratings]
    
    return {
        "user_id": user_id,
        "total_ratings": len(user_ratings),
        "average_rating": round(np.mean(ratings_list), 2),
        "in_training_data": user_id in user_map,
        "recommendation_type": "personalized" if len(user_ratings) >= 5 and user_id in user_map else "cold_start"
    }

# ────────────────────────────────────────────────
# Startup message
# ────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    print("\n" + "="*60)
    print("🎬 Movie Recommender API Started Successfully!")
    print("="*60)
    print(f"📊 Model: FunkSVD")
    print(f"👥 Users in training: {len(user_map):,}")
    print(f"🎥 Movies in catalog: {len(movie_map):,}")
    print(f"⭐ Total ratings: {len(ratings):,}")
    print("="*60)
    print("\n📝 API Documentation: http://localhost:8000/docs")
    print("🔄 Health check: http://localhost:8000/\n")

# ────────────────────────────────────────────────
# Run with: uvicorn app:app --reload
# Or: python -m uvicorn app:app --reload --port 8000
# ────────────────────────────────────────────────