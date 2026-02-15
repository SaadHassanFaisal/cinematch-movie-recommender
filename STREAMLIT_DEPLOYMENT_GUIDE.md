# 🎬 CineMatch - Streamlit UI Deployment Guide

## 🎨 Design Philosophy: Cinematic Noir Elegance

This UI is designed with **professional-grade aesthetics** inspired by luxury cinema:

### Visual Identity
- **Typography**: Playfair Display (elegant serif) + Inter (clean sans-serif)
- **Color Palette**: 
  - Noir blacks (#0a0a0a, #1a1a1a)
  - Luxurious gold (#d4af37, #f4e4a6)
  - Midnight blues for depth
  - Silver accents for sophistication
- **Design Language**: Film noir meets modern luxury
- **Animations**: Smooth, cinematic transitions with hover effects
- **Layout**: Generous spacing, card-based design with depth

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install streamlit requests python-dotenv
```

### Step 2: Set Up Directory Structure
```
D:\Machine Learning Projects\10. Movie Recommender\
├── app.py                    # FastAPI backend (already running)
├── streamlit_app.py          # NEW: Streamlit UI
├── .env                      # NEW: Environment variables
├── .streamlit/
│   └── config.toml          # NEW: Streamlit theme config
└── requirements_streamlit.txt  # NEW: UI dependencies
```

### Step 3: Create .streamlit Directory
```bash
mkdir .streamlit
# Copy config.toml into .streamlit/
```

### Step 4: Set Environment Variables (Optional but Recommended)
```bash
# Copy .env.template to .env
cp .env.template .env

# Edit .env and add your TMDB API key
# Get free key from: https://www.themoviedb.org/settings/api
```

**Without TMDB API Key**: App will use placeholder images (still looks professional)
**With TMDB API Key**: Real movie posters for stunning visuals ✨

### Step 5: Start the UI
```bash
# Make sure FastAPI is running first:
# Terminal 1:
uvicorn app:app --reload

# Terminal 2:
streamlit run streamlit_app.py
```

Your app will open at: **http://localhost:8501**

---

## 🎨 UI Features

### Page 1: Welcome Screen
- **Cinematic hero section** with gradient gold title
- **Two paths**:
  - New users: Auto-generate ID and start onboarding
  - Returning users: Enter existing ID
- **Elegant animations** on page load

### Page 2: Onboarding (New Users)
- **Visual progress bar** showing rating progress (5 required)
- **Grid of 20 popular movies** with posters
- **Star rating system** for each movie (0.5 - 5.0 stars)
- **Hover effects** on movie cards with gold glow
- **Submit button** unlocks after 5 ratings

### Page 3: Recommendations Dashboard
- **User statistics cards**:
  - Total films rated
  - Average rating
  - Recommendation mode (Personalized/Popular)
  - Training data status
- **Customizable grid** (5-30 recommendations)
- **Movie cards** with:
  - High-quality posters (if TMDB key provided)
  - Film title in elegant serif font
  - Genre tags
  - Predicted rating badges (gold)
- **Hover effects**: Cards lift and glow on hover
- **Refresh and Home buttons** for navigation

---

## 🎨 Customization Options

### Change Color Scheme
Edit the CSS variables in `streamlit_app.py`:

```python
:root {
    --noir-black: #0a0a0a;        # Main background
    --gold-accent: #d4af37;       # Primary accent
    --gold-light: #f4e4a6;        # Lighter gold for text
    --midnight-blue: #0f1419;     # Gradient background
    --silver: #c0c0c0;            # Secondary text
}
```

### Change Typography
Replace fonts in the `@import` statement:
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display...');
```

Popular alternatives:
- **Serif**: Crimson Pro, Cormorant, Libre Baskerville
- **Sans**: Poppins, Montserrat, Work Sans

### Adjust Layout
Modify grid columns:
```python
cols_per_row = 4  # Change from 4 to 3, 5, or 6
```

---

## 🖼️ TMDB API Setup (Recommended)

### Why Use TMDB?
- **Real movie posters** instead of placeholders
- **Professional appearance**
- **Free tier available** (1000+ requests/day)

### Get Your API Key
1. Go to https://www.themoviedb.org/
2. Create free account
3. Go to Settings → API
4. Request API key (choose "Developer")
5. Copy your API Key (v3 auth)

### Add to .env File
```bash
TMDB_API_KEY=your_actual_key_here
```

### Test It's Working
```python
# In Python console:
import os
print(os.getenv("TMDB_API_KEY"))  # Should print your key
```

---

## 📊 Performance Optimization

### Caching Posters (Optional)
Add caching to avoid repeated TMDB calls:

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_movie_poster(title: str) -> str:
    # ... existing code ...
```

### Lazy Loading Images
For very large grids, consider pagination:

```python
# Instead of showing all 30 movies at once
page_size = 10
page = st.number_input("Page", 1, (len(recs) // page_size) + 1)
start_idx = (page - 1) * page_size
end_idx = start_idx + page_size
display_recs = recs[start_idx:end_idx]
```

---

## 🚀 Deployment Options

### Option 1: Streamlit Community Cloud (FREE)
**Best for**: Quick demos, portfolios

1. Push code to GitHub:
```bash
git add streamlit_app.py .streamlit/config.toml requirements_streamlit.txt
git commit -m "Add Streamlit UI"
git push
```

2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repo
5. Set main file: `streamlit_app.py`
6. Add secrets (TMDB_API_KEY) in Settings
7. Deploy!

**Note**: You'll need to deploy FastAPI separately (see below)

### Option 2: Heroku (FastAPI + Streamlit)
**Best for**: Production apps

**Deploy FastAPI:**
```bash
# Create Procfile
echo "web: uvicorn app:app --host=0.0.0.0 --port=${PORT:-8000}" > Procfile

# Deploy
heroku create my-movie-api
git push heroku main
```

**Deploy Streamlit:**
```bash
# Update API_URL in .env to Heroku URL
API_URL=https://my-movie-api.herokuapp.com

# Create new Heroku app for Streamlit
echo "web: streamlit run streamlit_app.py" > Procfile_streamlit
heroku create my-movie-ui
git push heroku main
```

### Option 3: AWS/GCP/Azure
- **EC2/Compute Engine/VM**: Run both services on same server
- **Docker**: Containerize both apps (see Docker section below)
- **Serverless**: API on Lambda/Cloud Functions, UI on Streamlit Cloud

---

## 🐳 Docker Deployment

### Dockerfile for Streamlit
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt

COPY streamlit_app.py .
COPY .streamlit/ .streamlit/

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose (Both Services)
```yaml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models
    volumes:
      - ./models:/app/models

  ui:
    build: ./ui
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
      - TMDB_API_KEY=${TMDB_API_KEY}
    depends_on:
      - api
```

Run:
```bash
docker-compose up
```

---

## 🎭 Advanced Features to Add

### 1. User Authentication
```python
import streamlit_authenticator as stauth

# Add login system
authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')
```

### 2. Search Functionality
```python
search_query = st.text_input("🔍 Search movies...")
if search_query:
    # Filter recommendations by title
    filtered = [m for m in recs if search_query.lower() in m['title'].lower()]
```

### 3. Filter by Genre
```python
selected_genres = st.multiselect("Filter by genre:", 
    ["Action", "Drama", "Comedy", "Sci-Fi", ...])
```

### 4. Rating History
```python
# Add page to show all user's ratings
if st.button("View My Ratings"):
    # Fetch from database, display in table
```

### 5. Social Features
```python
# Share recommendations
if st.button("Share"):
    share_link = f"https://myapp.com/?recs={rec_ids}"
    st.code(share_link)
```

---

## 🐛 Troubleshooting

### Issue: Placeholders instead of posters
**Solution**: Add TMDB API key to .env

### Issue: API connection error
**Solution**: Verify FastAPI is running on port 8000
```bash
curl http://localhost:8000/
```

### Issue: Slow loading
**Solution**: 
1. Enable poster caching with `@st.cache_data`
2. Reduce number of recommendations
3. Use pagination

### Issue: Styles not applying
**Solution**: Clear browser cache and Streamlit cache
```bash
streamlit cache clear
```

### Issue: Layout broken on mobile
**Solution**: Add responsive CSS
```css
@media (max-width: 768px) {
    .movie-card {
        width: 100% !important;
    }
}
```

---

## 📸 Screenshots for Portfolio

### Recommended Screenshots
1. **Hero/Welcome page** - Shows elegant title and CTAs
2. **Onboarding grid** - 20 movie cards with star ratings
3. **Recommendations page** - Stats cards + movie grid
4. **Hover effect** - Movie card with gold glow
5. **Mobile view** - Responsive design

### How to Capture
```bash
# Full page screenshot
streamlit run streamlit_app.py --server.headless=true
# Use browser dev tools (Cmd+Shift+P → Screenshot)
```

---

## 🎬 Demo GIF Creation

Use **LICEcap** or **ScreenToGif**:

1. Start recording
2. Navigate: Welcome → Onboarding → Rate 5 movies → Recommendations
3. Hover over a few cards (show the glow effect)
4. Stop recording
5. Optimize GIF size: https://ezgif.com/optimize

Add to README:
```markdown
![Demo](demo.gif)
```

---

## 📝 README Template for GitHub

```markdown
# 🎬 CineMatch - AI Movie Recommender

Personalized movie recommendations powered by collaborative filtering.

![Demo](demo.gif)

## Features
- 🎨 Luxury noir-inspired UI
- 🤖 FunkSVD collaborative filtering
- 📊 Real-time recommendations
- ⭐ Interactive rating system
- 🎬 TMDB movie posters

## Tech Stack
- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: Streamlit + Custom CSS
- **ML**: NumPy (matrix factorization)
- **Data**: MovieLens 1M

## Quick Start
\```bash
# Install dependencies
pip install -r requirements.txt

# Start API
uvicorn app:app --reload

# Start UI (new terminal)
streamlit run streamlit_app.py
\```

## Live Demo
🔗 [Try it here](https://your-app.streamlit.app)

## Architecture
![Architecture](architecture.png)

## Results
- 55× faster recommendations vs naive approach
- <100ms response time
- 9/9 tests passing

## License
MIT
```

---

## 🎯 Next Steps After UI Launch

1. **Gather User Feedback**
   - Add analytics (Google Analytics)
   - Track which movies get rated most
   - Monitor API performance

2. **Iterate on Design**
   - A/B test color schemes
   - Try different layouts
   - Test mobile responsiveness

3. **Add More Features**
   - Movie search
   - Genre filters
   - Watchlist functionality
   - User profiles with avatars

4. **Performance Optimization**
   - CDN for static assets
   - Redis caching for API
   - Database connection pooling

5. **SEO & Marketing**
   - Add meta tags for social sharing
   - Create landing page
   - Write blog post about the project

---

## 🌟 Making It Portfolio-Ready

### LinkedIn Post Template
```
🎬 Excited to share my latest ML project: CineMatch!

Built a full-stack movie recommendation system with:
• Collaborative filtering (FunkSVD)
• FastAPI backend (55× performance improvement)
• Luxury Streamlit UI with custom CSS
• Real-time personalization

Tech: Python, NumPy, SQLAlchemy, Streamlit

Live demo: [link]
GitHub: [link]

#MachineLearning #Python #DataScience #WebDev
```

### What Recruiters Look For
✅ **Clean, professional UI** - This design stands out
✅ **Working demo** - Deploy to Streamlit Cloud
✅ **Good documentation** - README with architecture
✅ **Performance metrics** - "55× faster" is impressive
✅ **Full-stack** - Shows frontend + backend + ML skills

---

## 💎 Why This Design Works

1. **Professional Aesthetic**: Noir + gold = luxury, not "bootcamp project"
2. **Attention to Detail**: Custom fonts, animations, hover effects
3. **User Experience**: Clear flow, progress indicators, instant feedback
4. **Scalability**: Clean code structure, easy to extend
5. **Memorable**: Distinctive style that stands out in portfolios

**This is not a generic Streamlit app - this is a statement piece.** 🎭

---

Need help with deployment? Want to customize the design? Let me know!
