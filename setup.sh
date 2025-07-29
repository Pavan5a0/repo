#!/bin/bash

# Telegram Movie Search Bot Setup Script

echo "🎬 Setting up Telegram Movie Search Bot..."
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Python found: $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip
pip_version=$(pip3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Pip found: $pip_version"
else
    echo "❌ Pip not found. Please install pip."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv movie_bot_env
source movie_bot_env/bin/activate
echo "✅ Virtual environment created and activated"

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Bot token setup
echo ""
echo "🤖 Bot Token Setup"
echo "=================="
echo "1. Go to https://t.me/botfather"
echo "2. Create a new bot with /newbot"
echo "3. Copy your bot token"
echo ""
read -p "Enter your Telegram Bot Token: " bot_token

if [ -n "$bot_token" ]; then
    # Set environment variable
    echo "export TELEGRAM_BOT_TOKEN='$bot_token'" >> ~/.bashrc
    export TELEGRAM_BOT_TOKEN="$bot_token"
    echo "✅ Bot token configured"
else
    echo "⚠️  No token entered. You can set it later with:"
    echo "   export TELEGRAM_BOT_TOKEN='your_token_here'"
fi

# Make script executable
chmod +x telegram_movie_bot.py

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🚀 To start the bot:"
echo "   source movie_bot_env/bin/activate"
echo "   python telegram_movie_bot.py"
echo ""
echo "📱 Bot Commands:"
echo "   /start - Welcome message"
echo "   /help  - Usage instructions" 
echo "   /stats - Usage statistics"
echo "   <movie_name> - Search for movies"
echo ""
echo "🎬 Happy movie searching!"