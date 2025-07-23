#!/bin/bash

# Try installing aria2 without sudo (Render doesn't allow sudo)
apt-get update -o Debug::pkgProblemResolver=yes -o Debug::Acquire::http=yes
apt-get install -y aria2 || echo "Aria2 installation failed, continuing anyway..."

# Start aria2 in the background if available
if command -v aria2c &> /dev/null; then
    aria2c \
        --enable-rpc \
        --rpc-listen-port=6800 \
        --rpc-secret=62cec009933c5b9e791e3e56cd9bc463 \
        --daemon \
        --log=/tmp/aria2.log \
        --check-certificate=false
else
    echo "Warning: aria2c not available, download features will be limited"
fi

# Start your Python bot
python3 terabox.py
