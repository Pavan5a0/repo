# 🎬 Telugu Movie Search Bot

A Telegram bot that searches for Telugu movies across multiple websites and returns working links. When a user sends a movie name, the bot searches across 4 popular Telugu movie websites and responds with available links or "Movie not found".

## 🚀 Features

- **Multi-site Search**: Searches across 4 Telugu movie websites simultaneously
- **Fast Concurrent Searching**: Uses async/await for parallel website checking
- **Smart Content Detection**: Analyzes page content to verify movie availability
- **User-friendly Interface**: Clean, emoji-rich responses with easy-to-use commands
- **Error Handling**: Robust error handling with timeout protection
- **Configurable**: Easy to modify search sites and parameters

## 🌐 Supported Websites

1. **TellyBiz** - `tellybiz.in`
2. **MP4Online** - `mp4online1.blogspot.com`
3. **MoviezWap** - `moviezwap.blue`
4. **iBomma** - `dev.ibomma.wf`

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Internet connection

## 🛠️ Installation

### 1. Clone or Download

Save the bot files to your local machine:
- `telegram_movie_bot.py` - Main bot file
- `config.py` - Configuration file
- `requirements.txt` - Dependencies

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### 4. Configure the Bot

Edit `config.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

## 🚀 Running the Bot

```bash
python telegram_movie_bot.py
```

You should see:
```
🚀 Starting Telugu Movie Search Bot...
Press Ctrl+C to stop the bot
```

## 💬 How to Use

### Commands

- `/start` - Welcome message and bot information
- `/help` - Detailed usage instructions

### Search for Movies

Simply send the movie name to the bot:

```
User: Salaar
Bot: 🔍 Searching for Salaar across Telugu movie sites...
     Please wait...

     🎬 Found Salaar!
     
     Working Links:
     1️⃣ TellyBiz
     🔗 https://tellybiz.in/search?q=Salaar
     
     2️⃣ iBomma
     🔗 https://dev.ibomma.wf/telugu-movies?q=Salaar
```

## ⚙️ Configuration

### Adding New Websites

Edit `config.py` to add more movie websites:

```python
MOVIE_WEBSITES = [
    # Existing websites...
    {
        "name": "New Site",
        "search_url": "https://newsite.com/search?q={}",
        "domain": "newsite.com"
    }
]
```

### Adjusting Search Parameters

```python
SEARCH_TIMEOUT = 10      # Total request timeout (seconds)
CONNECT_TIMEOUT = 5      # Connection timeout (seconds)
MIN_INDICATORS_FOR_MATCH = 3  # Minimum content indicators for movie match
```

## 🔧 Technical Details

### How It Works

1. **User Input**: User sends movie name to bot
2. **URL Generation**: Bot creates search URLs for each website
3. **Concurrent Requests**: Makes simultaneous HTTP requests to all sites
4. **Content Analysis**: Analyzes page content for movie-related keywords
5. **Result Processing**: Filters working links and formats response
6. **Response**: Sends formatted message with results

### Content Detection

The bot analyzes webpage content for these indicators:
- Movie name (exact match)
- Keywords: "download", "watch", "movie", "telugu", "hd", "quality"
- Requires minimum 3 indicators for a positive match

### Error Handling

- **Timeout Protection**: 10-second total timeout, 5-second connection timeout
- **HTTP Error Handling**: Handles various HTTP status codes
- **Network Issues**: Graceful handling of network connectivity problems
- **Invalid Responses**: Validates and sanitizes all responses

## 📁 File Structure

```
telegram-movie-bot/
├── telegram_movie_bot.py   # Main bot application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛡️ Security Notes

- Never share your bot token publicly
- The bot doesn't store any user data
- All searches are performed in real-time
- No movie files are downloaded or stored

## 🐛 Troubleshooting

### Bot Won't Start

1. Check if bot token is correct in `config.py`
2. Verify internet connection
3. Ensure all dependencies are installed

### No Search Results

1. Check if movie name spelling is correct
2. Try shorter or alternative movie names
3. Verify websites are accessible
4. Check bot logs for error messages

### Timeout Errors

1. Increase `SEARCH_TIMEOUT` in `config.py`
2. Check internet connection speed
3. Some websites might be temporarily down

## 🔄 Updates and Maintenance

### Updating Movie Websites

If a website changes its URL structure:
1. Update the `search_url` in `config.py`
2. Restart the bot
3. Test with a known movie name

### Adding Features

The bot is designed to be easily extensible:
- Add more search websites
- Implement different content detection methods
- Add movie quality/format filtering
- Include user preferences and favorites

## 📝 Logging

The bot includes comprehensive logging:
- Search requests and responses
- Error messages and stack traces
- User interactions and commands

Logs are displayed in the console where the bot is running.

## ⚖️ Legal Disclaimer

This bot is for educational purposes only. It only searches and provides links to publicly available content. Users are responsible for complying with their local laws and the terms of service of the websites being searched.

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest new features
- Add more movie websites
- Improve content detection algorithms

---

**Happy movie searching! 🍿**
