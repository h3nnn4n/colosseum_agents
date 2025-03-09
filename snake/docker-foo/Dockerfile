FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the agent script executable
RUN chmod +x agent.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the agent directly (stdio approach)
CMD ["python", "agent.py"]