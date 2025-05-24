#!/usr/bin/env bash

# Install Node dependencies
npm install

# Install Python dependencies
pip3 install -r requirements.txt

# DEBUG: Show what's installed
echo "=== Installed Python packages ==="
pip3 list
