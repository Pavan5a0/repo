# Telugu Movie Search Telegram Bot

A Telegram bot that searches for Telugu movies on two different websites and returns matching links.

## Features

* Accepts full or partial movie names (minimum 3 characters)
* Searches two sources in parallel:
  * 🍿 **Bappam** – dynamic site, scraped with Selenium
  * 🎥 **MP4Online** – static site, fetched with `requests` + BeautifulSoup
* Sends up to 3 matching links per site back to the user
* Graceful error handling (invalid input, site errors, etc.)

## Requirements

* Python 3.9+
* Google Chrome installed (for headless Selenium)
* The packages listed in `requirements.txt`

## Setup

1. Clone the repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a new Telegram bot with [BotFather](https://t.me/BotFather) and copy the token.
3. Copy `.env.example` to `.env` (or export the variable some other way) and set `TELEGRAM_BOT_TOKEN`:

   ```bash
   echo "TELEGRAM_BOT_TOKEN=123456:ABC-DEF" > .env
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

Send any movie name (>=3 letters) to your bot. Example:

```
User → pushpa
Bot  → ✅ Found matches:
        🍿 Bappam:
        • https://…/Pushpa-2021…

        🎥 MP4Online:
        • https://…/pushpa-telugu.html?m=1
```
