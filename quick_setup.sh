#!/bin/bash

echo "🎬 Quick Telegram Bot Setup"
echo "=========================="
echo ""
echo "📱 Step 1: Get Your Bot Token"
echo "1. Open Telegram app"
echo "2. Search for @BotFather"
echo "3. Send /newbot"
echo "4. Choose a name like 'MyMovieBot'"
echo "5. Choose a username like 'mymoviebot_123'"
echo "6. Copy the token (looks like: 123456789:ABCdef...)"
echo ""

read -p "🔑 Paste your bot token here: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ No token entered. Exiting..."
    exit 1
fi

echo ""
echo "💾 Setting up your bot..."

# Update config.py with the token
if [ -f "config.py" ]; then
    # Create a backup
    cp config.py config.py.backup
    
    # Replace the token in config.py
    sed -i "s/YOUR_BOT_TOKEN_HERE/$BOT_TOKEN/g" config.py
    
    echo "✅ Bot token saved to config.py"
else
    echo "❌ config.py not found!"
    exit 1
fi

# Set environment variable for current session
export TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
echo "✅ Environment variable set"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🚀 Start your bot:"
echo "   python telegram_movie_bot.py"
echo ""
echo "📱 Test your bot:"
echo "   1. Go to Telegram"
echo "   2. Search for your bot's username"
echo "   3. Send /start"
echo "   4. Try searching: Avatar"
echo ""
echo "🎬 Happy movie searching!"