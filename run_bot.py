#!/usr/bin/env python3
"""
Simple runner script for the Telugu Movie Search Bot
"""

import sys
import os

def main():
    """Run the Telugu Movie Search Bot"""
    print("🎬 Telugu Movie Search Bot Runner")
    print("=" * 40)
    
    # Check if config file exists
    if not os.path.exists('config.py'):
        print("❌ Error: config.py not found!")
        print("Please make sure config.py exists and contains your BOT_TOKEN")
        return
    
    # Import and check bot token
    try:
        from config import BOT_TOKEN
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("❌ Error: Please set your BOT_TOKEN in config.py")
            print("Get your token from @BotFather on Telegram")
            return
    except ImportError:
        print("❌ Error: Could not import BOT_TOKEN from config.py")
        return
    
    # Check if main bot file exists
    if not os.path.exists('telegram_movie_bot.py'):
        print("❌ Error: telegram_movie_bot.py not found!")
        return
    
    print("✅ Configuration looks good!")
    print("🚀 Starting the bot...")
    print("")
    
    # Import and run the bot
    try:
        from telegram_movie_bot import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == '__main__':
    main()