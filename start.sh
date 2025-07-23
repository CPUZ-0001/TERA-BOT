#!/bin/bash

# Install aria2 if not present (Render.com specific)
if ! command -v aria2c &> /dev/null; then
    echo "Installing aria2..."
    apt-get update && apt-get install -y aria2
fi

# Start aria2 in background with RPC enabled
aria2c \
    --enable-rpc \
    --rpc-listen-all=false \
    --rpc-listen-port=6800 \
    --rpc-allow-origin-all \
    --daemon \
    --log=/var/log/aria2.log \
    --check-certificate=false

# Start your Python bot
python3 terabox.py
