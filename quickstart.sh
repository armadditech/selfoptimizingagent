#!/bin/bash
# Quickstart script for Self-Optimizing Customer Service Agent

set -e

echo "=================================="
echo "  Self-Optimizing Agent Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Copy configuration
echo "Setting up configuration..."
if [ ! -f "config/config.json" ]; then
    cp config/config.example.json config/config.json
    echo "✓ Configuration file created: config/config.json"
    echo "  Please edit this file with your API key and settings"
else
    echo "✓ Configuration file already exists"
fi
echo ""

# Copy environment file
echo "Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Environment file created: .env"
    echo "  Please add your ANTHROPIC_API_KEY"
else
    echo "✓ Environment file already exists"
fi
echo ""

# Create data directories
echo "Creating data directories..."
mkdir -p data/conversations
mkdir -p data/analytics
mkdir -p data/optimizations
mkdir -p data/feedback
mkdir -p data/knowledge_base
mkdir -p logs
echo "✓ Data directories created"
echo ""

# Check for API key
echo "Checking for API key..."
if grep -q "your_api_key_here" .env 2>/dev/null; then
    echo "⚠️  ATTENTION: You need to set your ANTHROPIC_API_KEY"
    echo "   Edit .env file and add your API key"
    echo ""
elif [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo "   Set it in .env file or export it"
    echo ""
else
    echo "✓ API key found"
    echo ""
fi

echo "=================================="
echo "  Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Set your ANTHROPIC_API_KEY in .env file"
echo "  2. Customize config/config.json for your business"
echo "  3. Run: python src/agent.py (interactive mode)"
echo "  4. Or run: python src/api_server.py (API server mode)"
echo ""
echo "Documentation:"
echo "  • README.md - Overview and features"
echo "  • CUSTOMIZATION.md - Customization guide"
echo ""
echo "Happy building! 🚀"
echo ""
