# Use Python 3.10 slim image
FROM python:3.10-slim

# Install Chrome and dependencies for Selenium
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the server
CMD ["python", "whatsapp_server.py"]