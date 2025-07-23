FROM python:3.9-slim

# Install aria2 and dependencies
RUN apt-get update && apt-get install -y aria2

# Create working directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Start both services
CMD ["sh", "-c", "aria2c --enable-rpc --rpc-listen-port=6800 --daemon && python3 terabox.py"]
