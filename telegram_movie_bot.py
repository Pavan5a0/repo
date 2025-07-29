#!/usr/bin/env python3
"""
Telegram Movie Search Bot
Searches for movies across multiple movie websites and returns working links.
"""

import logging
import asyncio
import aiohttp
import re
import time
from typing import List, Dict, Optional
from urllib.parse import quote_plus
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import configuration
from config import BOT_TOKEN, MOVIE_SITES, REQUEST_TIMEOUT, USER_AGENT, MAX_CONCURRENT_SEARCHES, ENABLE_USAGE_STATS

class MovieSearchBot:
    def __init__(self):
        self.session = None
        self.usage_count = {}  # Track usage per user
        self.rate_limit = {}   # Rate limiting per user
        self.last_search_time = {}  # Track last search time per user
    
    async def start_session(self):
        """Initialize aiohttp session for web requests"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            headers = {'User-Agent': USER_AGENT}
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limits (max 5 searches per minute)"""
        current_time = time.time()
        
        if user_id not in self.rate_limit:
            self.rate_limit[user_id] = []
        
        # Remove searches older than 1 minute
        self.rate_limit[user_id] = [
            timestamp for timestamp in self.rate_limit[user_id] 
            if current_time - timestamp < 60
        ]
        
        # Check if user has exceeded limit
        if len(self.rate_limit[user_id]) >= 5:
            return False
        
        # Add current search to rate limit tracker
        self.rate_limit[user_id].append(current_time)
        return True
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def search_movie_on_site(self, movie_name: str, site_name: str, site_url: str) -> Optional[str]:
        """Search for a movie on a specific website"""
        try:
            await self.start_session()
            
            # Build search URL based on site configuration
            site_config = MOVIE_SITES.get(site_name, {})
            site_url = site_config.get('url', site_url)
            search_param = site_config.get('search_param', 's')
            
            if search_param == 'q' and '?' in site_url:
                search_url = f"{site_url}&{search_param}={quote_plus(movie_name)}"
            else:
                separator = '&' if '?' in site_url else '?'
                search_url = f"{site_url}{separator}{search_param}={quote_plus(movie_name)}"
            
            # Make request to search URL
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Look for movie links in the page content
                    # This is a basic implementation - you might need to adjust based on actual site structure
                    movie_patterns = [
                        rf'href="([^"]*{re.escape(movie_name.lower())}[^"]*)"',
                        rf'href="([^"]*{re.escape(movie_name.replace(" ", "-").lower())}[^"]*)"',
                        rf'href="([^"]*{re.escape(movie_name.replace(" ", "").lower())}[^"]*)"'
                    ]
                    
                    for pattern in movie_patterns:
                        matches = re.findall(pattern, content.lower(), re.IGNORECASE)
                        if matches:
                            # Return the first valid movie link found
                            for match in matches:
                                if any(word in match.lower() for word in movie_name.lower().split()):
                                    # Construct full URL if it's a relative path
                                    if match.startswith('http'):
                                        return match
                                    else:
                                        return site_url.rstrip('/') + '/' + match.lstrip('/')
                    
                    # If no specific movie links found, return the search results page
                    if any(word.lower() in content.lower() for word in movie_name.split()):
                        return search_url
                        
        except Exception as e:
            logger.error(f"Error searching {site_name} for {movie_name}: {str(e)}")
        
        return None
    
    async def search_all_sites(self, movie_name: str) -> Dict[str, str]:
        """Search for movie across all configured sites"""
        results = {}
        
        # Create tasks for concurrent searching
        tasks = []
        for site_name, site_config in MOVIE_SITES.items():
            site_url = site_config.get('url', '')
            task = self.search_movie_on_site(movie_name, site_name, site_url)
            tasks.append((site_name, task))
        
        # Execute all searches concurrently with semaphore for rate limiting
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_SEARCHES)
        
        async def limited_search(site_name, task):
            async with semaphore:
                try:
                    result = await task
                    if result:
                        return site_name, result
                except Exception as e:
                    logger.error(f"Error with {site_name}: {str(e)}")
                return None
        
        # Run all searches concurrently
        search_results = await asyncio.gather(
            *[limited_search(site_name, task) for site_name, task in tasks],
            return_exceptions=True
        )
        
        # Process results
        for result in search_results:
            if result and not isinstance(result, Exception):
                site_name, link = result
                results[site_name] = link
        
        return results

# Initialize bot instance
movie_bot = MovieSearchBot()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
🎬 Welcome to Movie Search Bot! 🎬

Just send me a movie name and I'll search for it across multiple movie websites!

🔍 I search these sites:
• 5movierulz
• mp4online
• ibomma (Telugu movies)
• watchmovierulz

📝 Example: Just type "Avengers" or "RRR" and I'll find links for you!

⚡ Fast, reliable, and easy to use!
"""
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🔰 How to use this bot:

1️⃣ Send me any movie name
2️⃣ I'll search across 4 movie websites
3️⃣ You'll get working links if found
4️⃣ If not found, I'll let you know

💡 Tips:
• Use exact movie names for better results
• Try both English and regional names
• Be patient - searching takes a few seconds

🎯 Example searches:
- "Avatar"
- "RRR"
- "Spider-Man"
- "Pushpa"
"""
    await update.message.reply_text(help_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show usage statistics."""
    if not ENABLE_USAGE_STATS:
        await update.message.reply_text(
            "📊 Statistics are currently disabled.\n"
            "Contact the administrator to enable stats tracking."
        )
        return
    
    user_id = update.effective_user.id
    user_count = movie_bot.usage_count.get(user_id, 0)
    total_count = sum(movie_bot.usage_count.values())
    
    stats_text = f"""
📊 Bot Statistics:

Your searches: {user_count}
Total searches: {total_count}
Active users: {len(movie_bot.usage_count)}

🚀 Keep searching for more movies!
"""
    await update.message.reply_text(stats_text)

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle movie search requests."""
    user_id = update.effective_user.id
    movie_name = update.message.text.strip()
    
    # Check rate limiting
    if not movie_bot.check_rate_limit(user_id):
        await update.message.reply_text(
            "⚠️ Rate limit exceeded!\n"
            "You can search for movies maximum 5 times per minute.\n"
            "Please wait a moment and try again. ⏱️"
        )
        return
    
    # Update usage count if stats are enabled
    if ENABLE_USAGE_STATS:
        movie_bot.usage_count[user_id] = movie_bot.usage_count.get(user_id, 0) + 1
    
    if not movie_name:
        await update.message.reply_text("Please send me a movie name to search for!")
        return
    
    # Send searching message
    searching_msg = await update.message.reply_text(
        f"🔍 Searching for '{movie_name}' across movie websites...\n⏳ Please wait..."
    )
    
    try:
        # Search across all sites
        results = await movie_bot.search_all_sites(movie_name)
        
        if results:
            # Format the response with found links
            response = f"🎬 Found '{movie_name}' on {len(results)} website(s):\n\n"
            
            for site_name, link in results.items():
                site_config = MOVIE_SITES.get(site_name, {})
                emoji = site_config.get('emoji', '🔗')
                response += f"{emoji} {site_name.title()}: {link}\n\n"
            
            response += "✅ Click any link above to watch the movie!"
            
        else:
            response = f"❌ Movie '{movie_name}' not found on any website.\n\n"
            response += "💡 Try:\n"
            response += "• Different spelling\n"
            response += "• Full movie name\n" 
            response += "• Alternative titles\n"
            response += "• Regional language names"
        
        # Edit the searching message with results
        await searching_msg.edit_text(response, disable_web_page_preview=True)
        
    except Exception as e:
        logger.error(f"Error searching for movie {movie_name}: {str(e)}")
        await searching_msg.edit_text(
            f"❌ Sorry, there was an error searching for '{movie_name}'.\n"
            "Please try again later."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    print("🚀 Starting Movie Search Bot...")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    finally:
        # Clean up
        if movie_bot.session:
            asyncio.run(movie_bot.close_session())