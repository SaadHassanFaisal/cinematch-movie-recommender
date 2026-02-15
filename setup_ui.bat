@echo off
REM Quick Setup Script for CineMatch Streamlit UI
REM Run this from your project directory

echo.
echo ================================================================
echo   CINEMATCH - STREAMLIT UI SETUP
echo ================================================================
echo.

REM Create .streamlit directory
echo [1/5] Creating .streamlit directory...
if not exist ".streamlit" mkdir .streamlit
echo Done!
echo.

REM Copy config file
echo [2/5] Setting up Streamlit configuration...
copy config.toml .streamlit\config.toml
echo Done!
echo.

REM Create .env file if it doesn't exist
echo [3/5] Creating environment file...
if not exist ".env" (
    echo API_URL=http://localhost:8000 > .env
    echo TMDB_API_KEY= >> .env
    echo Created .env file. Please add your TMDB API key!
) else (
    echo .env already exists. Skipping...
)
echo.

REM Install dependencies
echo [4/5] Installing Streamlit dependencies...
pip install -r requirements_streamlit.txt
echo Done!
echo.

REM Final instructions
echo [5/5] Setup complete!
echo.
echo ================================================================
echo   NEXT STEPS:
echo ================================================================
echo.
echo 1. Get TMDB API Key (optional but recommended):
echo    https://www.themoviedb.org/settings/api
echo.
echo 2. Add your key to .env file:
echo    TMDB_API_KEY=your_key_here
echo.
echo 3. Make sure FastAPI is running in another terminal:
echo    uvicorn app:app --reload
echo.
echo 4. Start Streamlit:
echo    streamlit run streamlit_app.py
echo.
echo ================================================================
echo   Your app will open at: http://localhost:8501
echo ================================================================
echo.

pause
