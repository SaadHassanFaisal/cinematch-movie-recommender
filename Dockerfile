# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files *including* the script
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose dynamic port (Railway ignores but docs say it's nice)
EXPOSE ${PORT:-8000}

# Run the script (exec form is fine now—script handles expansion)
CMD ["./start.sh"]