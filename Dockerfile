FROM python:3.9-slim

# Install aria2
RUN apt-get update && \
    apt-get install -y aria2 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make start.sh executable
RUN chmod +x start.sh

# Run startup script
CMD ["bash", "start.sh"]
