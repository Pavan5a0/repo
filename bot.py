#!/usr/bin/env python3
"""Telegram bot that searches Bappam and MP4Online for Telugu movie/episode links.

Environment variable:
    BOT_TOKEN  Telegram bot token.

Dependencies are listed in requirements.txt.
"""
import asyncio
import logging
import os
import re
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ----------------------------- Search helpers ----------------------------- #

def _deduplicate(urls: List[str]) -> List[str]:
    """Preserve order while removing duplicates."""
    seen = set()
    unique = []
    for url in urls:
        if url not in seen:
            unique.append(url)
            seen.add(url)
    return unique


def search_bappam(query: str, base_url: str = "https://fans.bappam.gift") -> List[str]:
    """Search Bappam using Selenium because the page is dynamically loaded."""
    logger.info("Searching Bappam for %s", query)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    links: List[str] = []
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_page_load_timeout(20)
        driver.get(base_url)

        # Scroll to bottom to trigger lazy-loading of content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        anchors = driver.find_elements(By.TAG_NAME, "a")
        pattern = re.compile(r"/bo-[^/]+/.*?\.html$", re.IGNORECASE)

        for a in anchors:
            href = a.get_attribute("href") or ""
            text = (a.text or "").lower()
            if pattern.search(href) and query in text:
                # Normalise relative paths
                if href.startswith("/"):
                    href = base_url.rstrip("/") + href
                links.append(href)
    except Exception as exc:
        logger.warning("Error while searching Bappam: %s", exc)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    return _deduplicate(links)


def search_mp4online(query: str, base_url: str = "https://mp4online1.blogspot.com") -> List[str]:
    """Search MP4Online via static HTML using Requests + BeautifulSoup."""
    logger.info("Searching MP4Online for %s", query)
    links: List[str] = []
    try:
        resp = requests.get(base_url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        pattern = re.compile(r"-telugu\.html\?m=1$", re.IGNORECASE)

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True).lower()
            if pattern.search(href) and query in text:
                links.append(href)
    except Exception as exc:
        logger.warning("Error while searching MP4Online: %s", exc)

    return _deduplicate(links)


# --------------------------- Telegram callbacks --------------------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send greeting message."""
    await update.message.reply_text(
        "👋 Send me a movie or episode name (at least 3 letters) and I will try to find download links from Bappam and MP4Online."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user query message."""
    if not update.message:
        return

    query = update.message.text.strip().lower()

    if len(query) < 3:
        await update.message.reply_text("❌ Enter 3+ letters")
        return

    # Perform searches concurrently in separate threads (non-blocking for asyncio)
    bappam_task = asyncio.to_thread(search_bappam, query)
    mp4_task = asyncio.to_thread(search_mp4online, query)

    bappam_links, mp4_links = await asyncio.gather(bappam_task, mp4_task)

    # Trim to top 3 results per site
    bappam_links = bappam_links[:3]
    mp4_links = mp4_links[:3]

    if bappam_links or mp4_links:
        parts: List[str] = ["✅ Found matches:\n"]
        if bappam_links:
            parts.append("🍿 Bappam:")
            parts.extend(f"• {link}" for link in bappam_links)
            parts.append("")
        if mp4_links:
            parts.append("🎥 MP4Online:")
            parts.extend(f"• {link}" for link in mp4_links)
        await update.message.reply_text("\n".join(parts))
    else:
        await update.message.reply_text(f"❌ '{query}' not found on either site")


# ------------------------------- Entrypoint ------------------------------ #

async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Environment variable BOT_TOKEN is required")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    await application.initialize()
    logger.info("Bot started. Listening for messages…")
    await application.start()
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())