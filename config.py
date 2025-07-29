# Telegram Bot Configuration
# Get your bot token from @BotFather on Telegram

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Movie websites configuration
MOVIE_WEBSITES = [
    {
        "name": "TellyBiz",
        "search_url": "https://tellybiz.in/search?q={}",
        "domain": "tellybiz.in"
    },
    {
        "name": "MP4Online",
        "search_url": "https://mp4online1.blogspot.com/search?q={}",
        "domain": "mp4online1.blogspot.com"
    },
    {
        "name": "MoviezWap",
        "search_url": "https://www.moviezwap.blue/search?q={}",
        "domain": "moviezwap.blue"
    },
    {
        "name": "iBomma",
        "search_url": "https://dev.ibomma.wf/telugu-movies?q={}",
        "domain": "ibomma.wf"
    }
]

# Search configuration
SEARCH_TIMEOUT = 10  # seconds
CONNECT_TIMEOUT = 5  # seconds
MAX_CONCURRENT_SEARCHES = 4

# Content detection thresholds
MIN_INDICATORS_FOR_MATCH = 3