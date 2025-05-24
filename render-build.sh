#!/usr/bin/env bash

echo "=== Installing Node.js dependencies ==="
npm install

echo "=== Installing Python dependencies ==="
which python3
python3 --version
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "=== Installed Python packages ==="
pip3 list
