import os
import asyncio
import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Make sure to set TELEGRAM_TOKEN env variable

# Mapping of site name to a function that builds the search URL
def build_search_urls(movie_name: str) -> Dict[str, str]:
    """Return dict of site_name -> url to query for the movie."""
    q = requests.utils.quote(movie_name)
    return {
        # Blogspot based site search
        "mp4online1": f"https://mp4online1.blogspot.com/search?q={q}&m=1",
        # 5movierulz search (WordPress style search)
        "5movierulz": f"https://www.5movierulz.sarl/?s={q}",
        # watchmovierulz search
        "watchmovierulz": f"https://www.watchmovierulz.fi/?s={q}",
        # ibomma search
        "ibomma": f"https://rts.ibomma.wf/?s={q}"
    }


def page_contains_movie(html: str, movie_name: str) -> bool:
    """A naive check: Does the HTML contain the movie name (case-insensitive)?"""
    return movie_name.lower() in html.lower()


def check_movie_on_site(url: str, movie_name: str, timeout: int = 10) -> bool:
    """Return True if movie appears present on the given URL."""
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200 and page_contains_movie(resp.text, movie_name):
            return True
    except Exception as e:
        logger.warning("Error querying %s: %s", url, e)
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a movie name and I'll look it up for you.")


# In-memory usage counter
usage_counter: Dict[int, int] = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    text = update.message.text.strip()
    if not text:
        return

    # Update usage counter
    usage_counter[user_id] = usage_counter.get(user_id, 0) + 1
    logger.info("User %s used bot %d times", user_id, usage_counter[user_id])

    movie_name = text
    await update.message.reply_chat_action(action="typing")

    search_urls = build_search_urls(movie_name)
    found_links: List[str] = []

    # Perform search sequentially (could be parallelized but keep simple)
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, check_movie_on_site, url, movie_name) for url in search_urls.values()]
    results = await asyncio.gather(*tasks)

    for (site_key, url), found in zip(search_urls.items(), results):
        if found:
            found_links.append(url)

    if found_links:
        reply = "\n".join(found_links)
    else:
        reply = "Movie not found"

    # Append usage info
    reply += f"\n\n(You've used this bot {usage_counter[user_id]} times.)"

    await update.message.reply_text(reply)


async def main():
    if not TOKEN:
        raise RuntimeError("Please set the TELEGRAM_TOKEN environment variable.")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())