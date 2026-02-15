# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose the port (Railway ignores this but it's good for docs/local testing)
EXPOSE ${PORT:-8000}

# Start command – shell form for $PORT expansion (no [] brackets!)
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}