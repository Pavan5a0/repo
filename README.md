# 🎬 Telegram Movie Search Bot

A powerful Telegram bot that searches for movies across multiple movie websites and returns working links instantly!

## 🌟 Features

- **Multi-Site Search**: Searches across 4 popular movie websites
- **Fast & Concurrent**: Searches all sites simultaneously for quick results
- **Usage Tracking**: Track bot usage with statistics
- **User-Friendly**: Simple commands and beautiful emoji responses
- **Error Handling**: Robust error handling and logging
- **Async Architecture**: High-performance asynchronous design

## 🎯 Supported Movie Sites

- 🎭 **5movierulz** - https://www.5movierulz.sarl/
- 📱 **mp4online** - https://mp4online1.blogspot.com/?m=1
- 🎪 **ibomma** - https://rts.ibomma.wf/telugu-movies/ (Telugu movies)
- 🎦 **watchmovierulz** - https://www.watchmovierulz.fi/

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

**Option A: Environment Variable (Recommended)**
```bash
export TELEGRAM_BOT_TOKEN="your_actual_bot_token_here"
```

**Option B: Edit the config file**
```python
# Edit config.py
BOT_TOKEN = "your_actual_bot_token_here"
```

### 4. Run the Bot

```bash
python telegram_movie_bot.py
```

## 📱 How to Use

1. **Start the bot**: Send `/start` to get welcome message
2. **Search movies**: Just type any movie name (e.g., "Avengers", "RRR")
3. **Get help**: Send `/help` for usage instructions
4. **View stats**: Send `/stats` to see usage statistics

### Example Usage

```
User: Avatar
Bot: 🔍 Searching for 'Avatar' across movie websites...
     ⏳ Please wait...

Bot: 🎬 Found 'Avatar' on 3 website(s):

     🎭 5movierulz: https://www.5movierulz.sarl/avatar-movie
     📱 mp4online: https://mp4online1.blogspot.com/avatar
     🎦 watchmovierulz: https://www.watchmovierulz.fi/avatar

     ✅ Click any link above to watch the movie!
```

## 🛠️ Files Structure

```
├── telegram_movie_bot.py    # Main bot script
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script
└── README.md              # This file
```

## ⚙️ Configuration Options

Edit `config.py` to customize:

- **BOT_TOKEN**: Your Telegram bot token
- **MOVIE_SITES**: Add/remove movie websites
- **REQUEST_TIMEOUT**: HTTP request timeout (default: 30s)
- **USER_AGENT**: Browser user agent string
- **MAX_CONCURRENT_SEARCHES**: Max concurrent site searches
- **ENABLE_USAGE_STATS**: Enable/disable usage tracking

## 🎯 Bot Commands

- `/start` - Welcome message and bot introduction
- `/help` - Detailed usage instructions
- `/stats` - View usage statistics
- `<movie_name>` - Search for any movie across all sites

## 🔧 Advanced Features

### Usage Tracking
The bot tracks how many times each user searches for movies:
- Per-user search count
- Total searches across all users
- Active user count

### Error Handling
- Network timeout protection
- Graceful failure handling
- Comprehensive logging
- User-friendly error messages

### Performance
- Asynchronous HTTP requests
- Concurrent site searching
- Efficient session management
- Optimized response times

## 🛡️ Security Notes

1. **Keep your bot token secure** - Never commit it to version control
2. **Use environment variables** for sensitive configuration
3. **Monitor bot usage** to prevent abuse
4. **Regular updates** - Keep dependencies updated

## 🚨 Legal Disclaimer

This bot is for educational purposes only. Users are responsible for:
- Complying with local laws regarding movie streaming
- Respecting copyright and intellectual property rights
- Using the bot responsibly and ethically

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot token is correct
- Verify internet connection
- Check bot permissions in Telegram

**No movie results:**
- Try different movie name spellings
- Check if movie websites are accessible
- Verify network connectivity

**Installation errors:**
- Update pip: `pip install --upgrade pip`
- Use Python 3.8+: `python --version`
- Install in virtual environment

### Getting Help

1. Check the logs for error messages
2. Verify all dependencies are installed
3. Test with a simple movie name like "Avatar"
4. Ensure bot token is valid and active

## 📊 Performance

- **Search Speed**: ~3-5 seconds per movie
- **Concurrent Sites**: All 4 sites searched simultaneously
- **Memory Usage**: Low memory footprint
- **Scalability**: Handles multiple users efficiently

## 🔮 Future Enhancements

- [ ] Add more movie websites
- [ ] Implement movie quality detection
- [ ] Add download size information
- [ ] Movie posters and descriptions
- [ ] User favorite movies list
- [ ] Advanced search filters
- [ ] Support for TV shows/series

## 📝 License

This project is for educational purposes. Use responsibly and in compliance with local laws.

---

**Happy Movie Searching! 🍿🎬**
