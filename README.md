# 🎬 Telegram Movie Search Bot

A Telegram bot that searches for movies across multiple websites and returns working links.

## 🎯 What it does:

1. **User sends movie name** → Example: "RRR"
2. **Bot searches 4 websites** → Creates search URLs and checks each site
3. **Returns working links** → If movie found, shows clickable links
4. **Or says "not found"** → If movie not available on any site

## 🚀 Quick Setup:

### 1. Get Telegram Bot Token
1. Open Telegram and find **@BotFather**
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My Movie Search Bot")
4. Choose a username (e.g., "my_movie_search_bot")
5. Copy the **bot token** you receive

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Bot Token
Open `movie_bot.py` and replace this line:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```
With your actual token:
```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4. Run the Bot
```bash
python movie_bot.py
```

## 📱 How to Use:

1. **Start the bot** → Send `/start` in Telegram
2. **Search movies** → Just type any movie name like:
   - RRR
   - Pushpa  
   - KGF
   - Baahubali

3. **Get results** → Bot will reply with:
   - ✅ Working links if movie found
   - ❌ "Movie not found" if not available

## 🌐 Websites Searched:

The bot searches these 4 movie websites:
- tellybiz.in
- mp4online1.blogspot.com  
- moviezwap.blue
- dev.ibomma.wf

## 🔧 How It Works:

```
User: "RRR"
  ↓
Bot creates URLs:
  → https://tellybiz.in/search?q=RRR
  → https://mp4online1.blogspot.com/search?q=RRR
  → https://www.moviezwap.blue/search?q=RRR
  → https://dev.ibomma.wf/telugu-movies?q=RRR
  ↓
Bot checks each website:
  → ✅ Site loads + contains "RRR" = Keep link
  → ❌ Site fails/no movie = Skip
  ↓
Bot replies:
  → Found links OR "Movie not found"
```

## ⚠️ Important Notes:

- **Legal Use**: Please ensure you use these websites legally and safely
- **Website Availability**: Some sites may be temporarily unavailable
- **Search Accuracy**: Bot looks for movie keywords in website content
- **Rate Limiting**: Bot has built-in delays to respect website servers

## 🛠️ Customization:

### Add More Websites:
Edit the `MOVIE_SITES` list in `movie_bot.py`:
```python
MOVIE_SITES = [
    "https://tellybiz.in/search?q=",
    "https://mp4online1.blogspot.com/search?q=",
    "https://www.moviezwap.blue/search?q=",
    "https://dev.ibomma.wf/telugu-movies?q=",
    "https://your-new-site.com/search?q="  # Add new sites here
]
```

### Modify Search Logic:
The `check_website()` function determines if a movie is found. You can adjust the keyword matching logic there.

## 🐛 Troubleshooting:

**Bot doesn't respond?**
- Check if bot token is correct
- Ensure bot is running (`python movie_bot.py`)

**"Movie not found" for existing movies?**
- Try different spelling
- Use original/English movie title
- Some websites may be temporarily down

**Import errors?**
- Install requirements: `pip install -r requirements.txt`
- Use Python 3.8+ version

## 📞 Support:

If you need help:
1. Check the error messages in terminal
2. Verify your bot token is correct  
3. Try different movie names
4. Restart the bot

---

Made with ❤️ for movie lovers! 🍿
