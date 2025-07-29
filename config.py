"""
Configuration file for Telegram Movie Search Bot
"""

import os

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Movie websites to search
MOVIE_SITES = {
    "5movierulz": {
        "url": "https://www.5movierulz.sarl/",
        "search_param": "s",
        "emoji": "🎭"
    },
    "mp4online": {
        "url": "https://mp4online1.blogspot.com/?m=1",
        "search_param": "q",
        "emoji": "📱"
    },
    "ibomma": {
        "url": "https://rts.ibomma.wf/telugu-movies/",
        "search_param": "s",
        "emoji": "🎪"
    },
    "watchmovierulz": {
        "url": "https://www.watchmovierulz.fi/",
        "search_param": "s",
        "emoji": "🎦"
    }
}

# Request settings
REQUEST_TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Bot settings
MAX_CONCURRENT_SEARCHES = 10
ENABLE_USAGE_STATS = True