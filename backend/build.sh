#!/bin/bash
set -e

echo "🚀 Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Build complete!"
