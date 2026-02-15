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

# Expose the port Railway will use (optional but good practice)
# You can keep 8000 or change to $PORT – both work
EXPOSE ${PORT:-8000}

# Start command – pick ONE of the options above
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}