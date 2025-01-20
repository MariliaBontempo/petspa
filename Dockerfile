FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy the backend code
COPY backend/ .

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 