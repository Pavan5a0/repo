import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from urllib.parse import quote_plus
import re
import asyncio
import aiohttp
from typing import List, Dict

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import configuration
try:
    from config import BOT_TOKEN, MOVIE_WEBSITES, SEARCH_TIMEOUT, CONNECT_TIMEOUT, MIN_INDICATORS_FOR_MATCH
except ImportError:
    # Fallback configuration if config.py doesn't exist
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
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
    SEARCH_TIMEOUT = 10
    CONNECT_TIMEOUT = 5
    MIN_INDICATORS_FOR_MATCH = 3

class MovieSearchBot:
    def __init__(self):
        self.session = None
    
    async def init_session(self):
        """Initialize aiohttp session with proper headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        timeout = aiohttp.ClientTimeout(total=SEARCH_TIMEOUT, connect=CONNECT_TIMEOUT)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=aiohttp.TCPConnector(ssl=False)
        )
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def check_movie_on_site(self, website: Dict[str, str], movie_name: str) -> Dict[str, str]:
        """
        Check if a movie exists on a specific website
        Returns dict with status and URL if found
        """
        try:
            # Create search URL
            encoded_movie = quote_plus(movie_name)
            search_url = website["search_url"].format(encoded_movie)
            
            logger.info(f"Searching on {website['name']}: {search_url}")
            
            # Make request to the website
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Check if the page contains movie-related content
                    movie_indicators = [
                        movie_name.lower(),
                        "download",
                        "watch",
                        "movie",
                        "telugu",
                        "hd",
                        "quality"
                    ]
                    
                    content_lower = content.lower()
                    
                    # Count how many indicators are found
                    indicator_count = sum(1 for indicator in movie_indicators if indicator in content_lower)
                    
                    # If we find enough indicators, consider it a match
                    if indicator_count >= MIN_INDICATORS_FOR_MATCH:
                        return {
                            "status": "found",
                            "url": search_url,
                            "site_name": website["name"]
                        }
                    else:
                        return {
                            "status": "not_found",
                            "url": search_url,
                            "site_name": website["name"],
                            "reason": f"Movie content not detected (indicators: {indicator_count}/6)"
                        }
                else:
                    return {
                        "status": "error",
                        "url": search_url,
                        "site_name": website["name"],
                        "reason": f"HTTP {response.status}"
                    }
                    
        except asyncio.TimeoutError:
            return {
                "status": "error",
                "url": search_url,
                "site_name": website["name"],
                "reason": "Timeout"
            }
        except Exception as e:
            return {
                "status": "error",
                "url": search_url,
                "site_name": website["name"],
                "reason": str(e)
            }
    
    async def search_movie_across_sites(self, movie_name: str) -> List[Dict[str, str]]:
        """
        Search for a movie across all configured websites
        Returns list of results
        """
        if not self.session:
            await self.init_session()
        
        # Create tasks for concurrent searching
        tasks = []
        for website in MOVIE_WEBSITES:
            task = self.check_movie_on_site(website, movie_name)
            tasks.append(task)
        
        # Execute all searches concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, dict):
                valid_results.append(result)
            else:
                logger.error(f"Error in search: {result}")
        
        return valid_results

# Initialize bot instance
movie_bot = MovieSearchBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
🎬 **Telugu Movie Search Bot** 🎬

Welcome! I can help you find Telugu movies across multiple websites.

**How to use:**
Just send me a movie name and I'll search for it across:
• TellyBiz
• MP4Online  
• MoviezWap
• iBomma

**Example:**
Send: `Salaar`
And I'll find working links for you!

**Commands:**
/start - Show this message
/help - Get help

Just type a movie name to get started! 🍿
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🔍 **How to search for movies:**

1️⃣ Simply type the movie name
Example: `RRR` or `Baahubali`

2️⃣ I'll search across 4 Telugu movie websites

3️⃣ You'll get working links or "Movie not found"

**Tips for better results:**
• Use the exact movie name
• Try both English and Telugu names
• Check spelling if no results found

**Supported sites:**
✅ TellyBiz
✅ MP4Online
✅ MoviezWap  
✅ iBomma

Need more help? Just ask! 😊
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle movie search requests"""
    movie_name = update.message.text.strip()
    
    if not movie_name:
        await update.message.reply_text("Please send a valid movie name! 🎬")
        return
    
    # Send "searching" message
    search_message = await update.message.reply_text(
        f"🔍 Searching for **{movie_name}** across Telugu movie sites...\nPlease wait...",
        parse_mode='Markdown'
    )
    
    try:
        # Search across all websites
        results = await movie_bot.search_movie_across_sites(movie_name)
        
        # Process results
        found_links = []
        failed_sites = []
        
        for result in results:
            if result["status"] == "found":
                found_links.append({
                    "site": result["site_name"],
                    "url": result["url"]
                })
            else:
                failed_sites.append({
                    "site": result["site_name"],
                    "reason": result.get("reason", "Unknown error")
                })
        
        # Prepare response message
        if found_links:
            response = f"🎬 **Found {movie_name}!**\n\n"
            response += "**Working Links:**\n"
            
            for i, link in enumerate(found_links, 1):
                response += f"{i}️⃣ **{link['site']}**\n"
                response += f"🔗 {link['url']}\n\n"
            
            if failed_sites:
                response += "**Sites that didn't have the movie:**\n"
                for site in failed_sites:
                    response += f"❌ {site['site']} - {site['reason']}\n"
        else:
            response = f"😔 **Movie not found: {movie_name}**\n\n"
            response += "The movie was not found on any of the searched sites:\n"
            for site in failed_sites:
                response += f"❌ {site['site']} - {site['reason']}\n"
            
            response += "\n**Tips:**\n"
            response += "• Check the spelling\n"
            response += "• Try the Telugu name\n"
            response += "• Try a shorter version of the name\n"
        
        # Edit the search message with results
        await search_message.edit_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error searching for movie {movie_name}: {e}")
        await search_message.edit_text(
            f"❌ **Error occurred while searching for {movie_name}**\n\n"
            f"Please try again later or contact support.\n"
            f"Error: {str(e)[:100]}...",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Start the bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: Please set your BOT_TOKEN in the script!")
        print("Get your token from @BotFather on Telegram")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Initialize bot session on startup
    async def post_init(application):
        await movie_bot.init_session()
    
    # Close session on shutdown  
    async def post_stop(application):
        await movie_bot.close_session()
    
    application.post_init = post_init
    application.post_stop = post_stop
    
    # Run the bot
    print("🚀 Starting Telugu Movie Search Bot...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == '__main__':
    main()