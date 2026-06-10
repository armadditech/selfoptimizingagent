#!/bin/bash
# Script to run the Self-Optimizing Agent Web UI

echo "======================================================================="
echo "  🤖 Self-Optimizing Customer Service Agent - Web UI"
echo "======================================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install flask flask-cors anthropic --quiet 2>&1 | grep -E "(Successfully|already|Requirement)" || true

echo ""
echo "======================================================================="
echo "  🚀 Starting Web UI"
echo "======================================================================="
echo ""
echo "Choose an option:"
echo ""
echo "  1) Basic Chat UI (port 5000)"
echo "  2) Enhanced UI with Simulator & Self-Optimization (port 5001)"
echo ""
read -p "Enter choice [1 or 2]: " choice

if [ "$choice" = "2" ]; then
    echo ""
    echo "Starting Enhanced UI..."
    echo ""
    echo "✨ Features:"
    echo "  • Interactive chat interface"
    echo "  • Customer interaction simulator"
    echo "  • Automated feedback collection"
    echo "  • Self-optimization engine"
    echo "  • A/B testing visualization"
    echo "  • Performance tracking"
    echo ""
    echo "🌐 Open your browser to: http://localhost:5001"
    echo ""
    echo "⏹  Press Ctrl+C to stop"
    echo ""
    python3 app_enhanced.py
else
    echo ""
    echo "Starting Basic Chat UI..."
    echo ""
    echo "✨ Features:"
    echo "  • Interactive chat"
    echo "  • Real-time analytics"
    echo "  • Intent visualization"
    echo ""
    echo "🌐 Open your browser to: http://localhost:5000"
    echo ""
    echo "⏹  Press Ctrl+C to stop"
    echo ""
    python3 app.py
fi
