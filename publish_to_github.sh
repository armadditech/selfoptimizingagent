#!/bin/bash

# 🚀 GitHub Publishing Script
# This script helps you publish your Self-Optimizing Agent to GitHub

set -e  # Exit on any error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚀 Publishing Self-Optimizing Agent to GitHub                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Final security check
echo "🔐 Step 1: Running final security check..."
echo ""

# Check for API keys in Python files (excluding documentation)
if git grep -i "sk-ant-" -- "*.py" "*.env" 2>/dev/null | grep -q .; then
    echo "❌ ERROR: Found potential API keys in code!"
    echo "   Please remove them before publishing."
    git grep -i "sk-ant-" -- "*.py" "*.env" 2>/dev/null
    exit 1
fi
echo "  ✅ No API keys found in code"

# Check .env is not staged
if [ -f .env ]; then
    echo "  ⚠️  WARNING: .env file exists (this is OK if not committed)"
fi

# Verify .gitignore exists
if [ -f .gitignore ]; then
    echo "  ✅ .gitignore present"
else
    echo "  ❌ ERROR: .gitignore missing!"
    exit 1
fi

echo ""

# Step 2: Initialize Git
echo "📦 Step 2: Initializing Git repository..."
if [ ! -d .git ]; then
    git init
    echo "  ✅ Git repository initialized"
else
    echo "  ✅ Git repository already initialized"
fi
echo ""

# Step 3: Get GitHub username
echo "👤 Step 3: GitHub Configuration"
echo ""
echo "What is your GitHub username?"
read -p "Username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ ERROR: GitHub username is required"
    exit 1
fi

echo ""
echo "What do you want to name your repository?"
echo "(Press Enter for default: SelfOptimizingAgent)"
read -p "Repository name: " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="SelfOptimizingAgent"
fi

REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo ""
echo "  Repository will be: $REPO_URL"
echo ""

# Step 4: Update README with username
echo "📝 Step 4: Updating README with your GitHub username..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/YOUR_USERNAME/${GITHUB_USERNAME}/g" README.md
    sed -i '' "s/yourusername/${GITHUB_USERNAME}/g" README.md
else
    # Linux
    sed -i "s/YOUR_USERNAME/${GITHUB_USERNAME}/g" README.md
    sed -i "s/yourusername/${GITHUB_USERNAME}/g" README.md
fi

echo "  ✅ README.md updated"
echo ""

# Step 5: Stage all files
echo "📦 Step 5: Staging files for commit..."
git add .
echo "  ✅ Files staged"
echo ""

echo "📊 Files to be committed:"
git status --short | head -20
echo ""

# Step 6: Commit
echo "💾 Step 6: Creating initial commit..."
git commit -m "Initial commit: Self-Optimizing Customer Service Agent

Features:
- AI-powered customer service with Claude API
- Real-time auto-optimization every 10 seconds
- Live conversation feed showing interactions
- Interactive demo mode (no API key required)
- Comprehensive documentation and security guidelines
- Production-ready with MIT license

Built with Python, Flask, and Claude AI (Anthropic)"

echo "  ✅ Initial commit created"
echo ""

# Step 7: Create GitHub repository instructions
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  📝 NEXT STEPS - Create GitHub Repository                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Before we can push, you need to create the repository on GitHub:"
echo ""
echo "1. Open this URL in your browser:"
echo "   👉 https://github.com/new"
echo ""
echo "2. Fill in the form:"
echo "   • Repository name: ${REPO_NAME}"
echo "   • Description: AI-powered customer service agent with real-time optimization"
echo "   • Public or Private: Your choice"
echo "   • ❌ Do NOT initialize with README (we have one)"
echo "   • ❌ Do NOT add .gitignore (we have one)"
echo "   • ❌ Do NOT add license (we have one)"
echo ""
echo "3. Click 'Create repository'"
echo ""
echo "4. Come back here and press Enter when done..."
read -p ""

# Step 8: Add remote and push
echo ""
echo "🚀 Step 8: Pushing to GitHub..."
echo ""

git branch -M main

if git remote | grep -q origin; then
    echo "  ⚠️  Remote 'origin' already exists, updating..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi

echo "  📡 Pushing to GitHub..."
echo ""

if git push -u origin main; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  🎉 SUCCESS! Your project is now on GitHub!                   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🌐 Your repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo ""
    echo "📝 Next steps:"
    echo ""
    echo "1. Add repository topics:"
    echo "   Go to your repo → ⚙️ Settings → Topics"
    echo "   Add: ai, customer-service, claude, anthropic, python, flask, chatbot"
    echo ""
    echo "2. Add a description:"
    echo "   Edit the 'About' section with:"
    echo "   'AI customer service agent that self-optimizes. Demo mode - no API key required!'"
    echo ""
    echo "3. Enable discussions (optional):"
    echo "   Settings → Features → Discussions"
    echo ""
    echo "4. Share your project:"
    echo "   Tweet it, post on Reddit, share on LinkedIn!"
    echo ""
    echo "🎭 Demo URL for others:"
    echo "   git clone https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
    echo "   cd ${REPO_NAME}"
    echo "   pip install -r requirements.txt"
    echo "   python demo_mode.py"
    echo ""
    echo "✨ Congratulations! 🎊"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo ""
    echo "1. Repository doesn't exist yet"
    echo "   → Create it at https://github.com/new"
    echo ""
    echo "2. Authentication failed"
    echo "   → You may need to set up a Personal Access Token"
    echo "   → See: https://docs.github.com/en/authentication"
    echo ""
    echo "3. Wrong repository name"
    echo "   → Make sure it matches: ${REPO_NAME}"
    echo ""
    echo "Try running these commands manually:"
    echo "   git remote -v  # Check remote URL"
    echo "   git push -u origin main  # Try push again"
    echo ""
fi
