#!/bin/bash

echo "▶️ Starting Aria2..."
aria2c --enable-rpc --rpc-listen-all=false --rpc-allow-origin-all --daemon

echo "⏳ Waiting for Aria2 to be ready..."
sleep 3

echo "🚀 Starting Bot..."
python3 terabox.py
