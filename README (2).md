# 🎬 CineMatch - AI-Powered Movie Recommender

> Personalized movie recommendations using collaborative filtering with a luxurious cinematic interface

[![Live Demo](https://img.shields.io/badge/Demo-Live-success?style=for-the-badge)](https://YOUR_APP.streamlit.app)
[![API](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge)](https://cinematch-api.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

## ✨ Features

- 🎯 **Personalized Recommendations** using FunkSVD collaborative filtering
- 🎨 **Luxury UI** with cinematic noir design (gold + black theme)
- ⚡ **Fast Performance** with aggressive caching (<100ms responses)
- 🔐 **Session Persistence** (24-hour login sessions)
- 📱 **Fully Responsive** on all devices
- 🎬 **Real Movie Posters** via TMDB API
- 📊 **User Analytics** dashboard with stats

---

## 🎥 Demo

### Welcome Screen
![Welcome](assets/welcome.png)

### Onboarding Flow
![Onboarding](assets/onboarding.png)

### Recommendations Dashboard
![Recommendations](assets/recommendations.png)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│               USER (Browser)                     │
└────────────────────┬─────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────┐
│         Streamlit Cloud (Port 8501)              │
│         • Session Management                     │
│         • User Interface                         │
│         • TMDB API Integration                   │
└────────────────────┬─────────────────────────────┘
                     │ HTTPS
                     ↓
┌──────────────────────────────────────────────────┐
│           Render.com (Port 8000)                 │
│         • FastAPI Backend                        │
│         • FunkSVD Model (6,040 × 3,706)         │
│         • SQLite Database                        │
└──────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- Streamlit 1.31
- Custom CSS (600+ lines)
- TMDB API integration

**Backend:**
- FastAPI 0.109
- SQLAlchemy ORM
- SQLite database

**ML Model:**
- FunkSVD (Matrix Factorization)
- NumPy for computation
- Training: MovieLens 1M dataset

---

## 🚀 Quick Start

### Live Demo
Try it now: **[cinematch.streamlit.app](https://YOUR_APP.streamlit.app)**

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/cinematch.git
cd cinematch

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_streamlit.txt

# Create .env file
echo "API_URL=http://localhost:8000" > .env
echo "TMDB_API_KEY=your_key_here" >> .env

# Start API
uvicorn app:app --reload

# Start UI (new terminal)
streamlit run streamlit_app.py
```

Visit:
- **UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Recommendation Speed** | <100ms |
| **Image Loading** | Batch pre-load (2-3s for 20 movies) |
| **Session Duration** | 24 hours |
| **API Response Time** | <50ms average |
| **Model Size** | ~50MB |
| **Test Coverage** | 9/9 tests passing (100%) |

### Key Optimizations
- **55× faster** than naive implementation
- **Aggressive caching**: 24h for posters, 5min for movies
- **Vectorized predictions** with NumPy
- **O(1) dictionary lookups** for movie mapping

---

## 🎯 Key Improvements from MVP

| Feature | Before | After |
|---------|--------|-------|
| Recommendation Speed | 2500ms | 45ms |
| Image Loading | Sequential (slow) | Parallel batch (fast) |
| Login Persistence | None | 24-hour sessions |
| User Validation | None | Checks existence |
| Error Handling | Basic | Production-ready |

---

## 📁 Project Structure

```
cinematch/
├── app.py                          # FastAPI backend
├── streamlit_app.py                # Streamlit UI
├── funksvd_model.npz               # Trained model
├── id_mappings.pkl                 # User/movie mappings
├── movies_metadata.csv             # Movie details
├── ratings_processed.csv           # Rating data
├── requirements.txt                # API dependencies
├── requirements_streamlit.txt      # UI dependencies
├── Procfile                        # Render deployment
├── runtime.txt                     # Python version
├── .streamlit/
│   └── config.toml                # Streamlit theme
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_modeling.ipynb
│   └── 03_evaluation.ipynb
└── tests/
    └── test_api.py                # API tests (9/9 passing)
```

---

## 🧪 Testing

### Run Tests
```bash
python test_api.py
```

**Results:** ✅ 9/9 tests passing (100%)

### Test Coverage
- ✅ Health check
- ✅ Rating submission & updates
- ✅ User validation
- ✅ Cold start recommendations
- ✅ Personalized recommendations
- ✅ Input validation (rating range, movie existence)
- ✅ Error handling (invalid IDs, API failures)

---

## 🎨 Design System

### Color Palette
```css
Primary:    Gold (#d4af37)
Background: Noir Black (#0a0a0a, #1a1a1a)
Accent:     Midnight Blue (#0f1419)
Text:       Silver (#c0c0c0), Gold Light (#f4e4a6)
```

### Typography
- **Headers**: Playfair Display (serif) - Elegant, cinematic
- **Body**: Inter (sans-serif) - Clean, readable

### Components
- Movie cards with 3D hover effects
- Gold gradient buttons with lift animation
- Stats dashboard cards
- Progress indicators
- Star rating sliders

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Content-based filtering (genres, cast, director)
- [ ] Hybrid recommendation model
- [ ] User profiles with avatars
- [ ] Social features (share recommendations, follow users)
- [ ] Advanced filters (genre, year, rating range)
- [ ] Watchlist functionality
- [ ] Email notifications for new recommendations

### Technical Improvements
- [ ] PostgreSQL migration (better concurrency)
- [ ] Redis caching layer
- [ ] A/B testing framework
- [ ] Real-time collaborative filtering
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [API Documentation](docs/API_DOCS.md) or visit `/docs` endpoint
- [Design System](docs/DESIGN_SYSTEM.md)
- [Bug Fixes Log](docs/BUG_FIXES.md)

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👤 Author

**Your Name**

- Portfolio: [yourwebsite.com](https://yourwebsite.com)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **MovieLens** for providing the dataset
- **TMDB** for movie poster API
- **Streamlit** for the amazing framework
- **FastAPI** for blazing-fast backend

---

## 📈 Project Timeline

- **Week 1**: Data preparation & EDA
- **Week 2**: Model training & evaluation
- **Week 3**: FastAPI backend development
- **Week 4**: Streamlit UI & deployment
- **Total**: 4 weeks from concept to production

---

## 🎓 What I Learned

### Technical Skills
- Matrix factorization for recommendations
- FastAPI for high-performance APIs
- Advanced Streamlit customization
- Production deployment strategies
- Performance optimization (55× speedup)

### Soft Skills
- Full-stack development workflow
- User experience design
- Error handling & edge cases
- Documentation best practices

---

<div align="center">
  <strong>Built with ❤️ and lots of ☕</strong>
  <br><br>
  <sub>If you found this project helpful, consider giving it a ⭐!</sub>
  <br><br>
  <a href="https://YOUR_APP.streamlit.app">
    <img src="https://img.shields.io/badge/Try%20Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo">
  </a>
</div>
