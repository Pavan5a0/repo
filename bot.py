import asyncio
import os
import re
import logging
from typing import List, Set

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update, constants
from telegram.ext import Application, ContextTypes, MessageHandler, filters
import time
import random

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ----------------------- CONFIG -----------------------
BAPPAM_URL = "https://fans.bappam.gift/telugu-movies/"
MP4ONLINE_SEARCH_URL = "https://mp4online1.blogspot.com/search?q={query}&m=1"
# Limit number of links per site in the reply
MAX_LINKS_PER_SITE = 3

# Regex patterns for filtering links
BAPPAM_LINK_RE = re.compile(r"/bo-[^/]+/.*?telugu-movie.*?\.html", re.IGNORECASE)
MP4ONLINE_LINK_RE = re.compile(r"\d{4}/\d{2}/.*?\.html\?m=1", re.IGNORECASE)

# -------------------- UTILITIES -----------------------

def deduplicate_links(links: List[str]) -> List[str]:
    seen: Set[str] = set()
    deduped: List[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            deduped.append(link)
    return deduped

# -------------------- SITE SCRAPERS --------------------

def search_bappam(query: str) -> List[str]:
    """Search the Bappam site for movies matching the query using Selenium."""
    logger.info("Starting Bappam search for query: %s", query)
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(BAPPAM_URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Scroll to the bottom to trigger lazy loading until no new content loads or cap reached
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        while scroll_attempts < 10:  # safety cap to avoid infinite loop
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1 + random.uniform(0, 0.5))  # brief wait for lazy-loaded content
            # Wait for new page height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1

        # After scrolling, collect links
        elements = driver.find_elements(By.TAG_NAME, "a")
        links: List[str] = []
        query_lower = query.lower()
        for el in elements:
            href = el.get_attribute("href")
            if not href:
                continue
            if query_lower in href.lower() and BAPPAM_LINK_RE.search(href):
                if href.startswith("/"):
                    href = f"https://fans.bappam.gift{href}"
                links.append(href)
        logger.info("Bappam search finished. Found %d links", len(links))
        return deduplicate_links(links)[:MAX_LINKS_PER_SITE]
    except Exception as exc:
        logger.warning("Error during Bappam search: %s", exc)
        return []
    finally:
        driver.quit()


def search_mp4online(query: str) -> List[str]:
    """Search MP4Online site using its Blogger search feature."""
    logger.info("Starting MP4Online search for query: %s", query)
    url = MP4ONLINE_SEARCH_URL.format(query=query)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        links: List[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if query.lower() in href.lower() and MP4ONLINE_LINK_RE.search(href):
                if href.endswith("?m=1"):
                    links.append(href)
                else:
                    links.append(f"{href}?m=1")
        logger.info("MP4Online search finished. Found %d links", len(links))
        return deduplicate_links(links)[:MAX_LINKS_PER_SITE]
    except Exception as exc:
        logger.warning("Error during MP4Online search: %s", exc)
        return []

# -------------------- TELEGRAM HANDLER --------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    query = update.message.text.strip().lower()
    if len(query) < 3:
        await update.message.reply_text("❌ Enter at least 3 letters")
        return

    await update.message.reply_chat_action(constants.ChatAction.TYPING)

    # Run site searches concurrently in thread executor to avoid blocking event loop
    loop = asyncio.get_running_loop()
    bappam_future = loop.run_in_executor(None, search_bappam, query)
    mp4_future = loop.run_in_executor(None, search_mp4online, query)

    bappam_links, mp4_links = await asyncio.gather(bappam_future, mp4_future)

    parts = []
    if bappam_links:
        parts.append("🍿 Bappam:\n" + "\n".join(f"• {link}" for link in bappam_links))
    if mp4_links:
        parts.append("🎥 MP4Online:\n" + "\n".join(f"• {link}" for link in mp4_links))

    if parts:
        reply = "✅ Found matches:\n\n" + "\n\n".join(parts)
    else:
        reply = f"❌ '{query}' not found on either site"

    await update.message.reply_text(reply)

# -------------------- MAIN ENTRY --------------------

def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Environment variable TELEGRAM_BOT_TOKEN is required")

    application = Application.builder().token(token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()