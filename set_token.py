#!/usr/bin/env python3
"""
Simple script to set Telegram bot token
"""

import os

def set_bot_token():
    print("🤖 Telegram Bot Token Setup")
    print("=" * 30)
    print()
    print("📝 Steps to get your bot token:")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot to create a new bot")
    print("3. Follow the instructions and choose a name")
    print("4. Copy the token that BotFather gives you")
    print()
    
    token = input("🔑 Paste your bot token here: ").strip()
    
    if not token or token == "YOUR_ACTUAL_BOT_TOKEN_HERE":
        print("❌ Invalid token. Please try again.")
        return
    
    # Method 1: Environment variable
    print()
    print("💾 Setting up bot token...")
    
    # Update config.py directly
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the token in config
        updated_content = content.replace(
            'BOT_TOKEN = os.getenv(\'TELEGRAM_BOT_TOKEN\', \'YOUR_BOT_TOKEN_HERE\')',
            f'BOT_TOKEN = os.getenv(\'TELEGRAM_BOT_TOKEN\', \'{token}\')'
        )
        
        with open('config.py', 'w') as f:
            f.write(updated_content)
        
        print("✅ Bot token saved to config.py")
        
        # Also set environment variable for current session
        os.environ['TELEGRAM_BOT_TOKEN'] = token
        print("✅ Environment variable set for current session")
        
        print()
        print("🚀 Your bot is now configured!")
        print("   Run: python telegram_movie_bot.py")
        
    except Exception as e:
        print(f"❌ Error saving token: {e}")
        print()
        print("🔧 Manual setup:")
        print(f"   Edit config.py and replace 'YOUR_BOT_TOKEN_HERE' with:")
        print(f"   '{token}'")

if __name__ == "__main__":
    set_bot_token()