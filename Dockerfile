# Use an official Python base image
FROM python:3.10-slim-buster as builder

# Set environment variables for dependencies installation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system-level dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

# Install Python dependencies in a layer to leverage caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app/

# Multi-stage build: Use a smaller base image for production
FROM python:3.10-slim-buster as runner

# Set environment variables for the application
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OLLAMA_API_KEY='' \
    OLLAMA_SERVER='http://localhost:11434' \
    OLLAMA_PROXY_PORT='11435' \
    OLLAMA_PROXY_HOST='0.0.0.0'

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the builder stage to reduce image size
COPY --from=builder /app .

# Expose the port where your Flask app will run
EXPOSE ${OLLAMA_PROXY_PORT}

# Command to run your Flask application
CMD ["python", "ollama-proxy.py"]