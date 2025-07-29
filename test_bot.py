#!/usr/bin/env python3
"""
Test script for Telegram Movie Search Bot
Verifies configuration and dependencies before running the bot.
"""

import sys
import os

def test_python_version():
    """Test if Python version is compatible"""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing dependencies...")
    required_packages = [
        'telegram',
        'aiohttp',
        'asyncio'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_configuration():
    """Test bot configuration"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import BOT_TOKEN, MOVIE_SITES
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("❌ Bot token not configured")
            print("Set TELEGRAM_BOT_TOKEN environment variable or edit config.py")
            return False
        
        print("✅ Bot token configured")
        print(f"✅ {len(MOVIE_SITES)} movie sites configured")
        
        for site_name, site_config in MOVIE_SITES.items():
            print(f"   📺 {site_name}: {site_config.get('url', 'No URL')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎬 Telegram Movie Search Bot - Test Suite")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_configuration
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    if passed == len(tests):
        print("🎉 All tests passed! Bot is ready to run.")
        print("\n🚀 Start the bot with:")
        print("   python telegram_movie_bot.py")
    else:
        print(f"❌ {len(tests) - passed} test(s) failed.")
        print("Please fix the issues before running the bot.")
    
    print("\n💡 Need help? Check the README.md file.")

if __name__ == "__main__":
    main()