#!/bin/bash
# Quick setup script for the website

echo "🚀 Setting up Shantara Pintak Website..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

echo ""

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
.venv/bin/pip install -q -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Build the site
echo "🔨 Building site..."
.venv/bin/python build.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  • Run dev server:    python dev.py"
echo "  • Build for prod:    python build.py"
echo "  • Edit content:      content.yaml"
echo "  • View local site:   open dist/index.html"
echo ""
