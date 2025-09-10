import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import aiohttp
from urllib.parse import quote
import re

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token - You need to get this from @BotFather on Telegram
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Movie websites to search
MOVIE_SITES = [
    "https://tellybiz.in/search?q=",
    "https://mp4online1.blogspot.com/search?q=",
    "https://www.moviezwap.blue/search?q=",
    "https://dev.ibomma.wf/telugu-movies?q="
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = """
🎬 Welcome to Movie Search Bot! 🎬

Just send me a movie name and I'll search for it across multiple websites!

Example: Send "RRR" or "Pushpa" and I'll find working links for you.

Type any movie name to get started! 🍿
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🆘 How to use this bot:

1️⃣ Send me any movie name
2️⃣ I'll search across 4 movie websites
3️⃣ I'll reply with working links if found
4️⃣ If not found, I'll tell you "Movie not found"

Examples:
• RRR
• Pushpa
• KGF
• Baahubali

Just type the movie name - no commands needed! 🎭
    """
    await update.message.reply_text(help_text)

async def check_website(session, url, movie_name):
    """Check if a website is accessible and likely contains the movie"""
    try:
        # Set timeout and headers
        timeout = aiohttp.ClientTimeout(total=10)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        async with session.get(url, timeout=timeout, headers=headers) as response:
            if response.status == 200:
                # Get page content
                content = await response.text()
                
                # Check if movie name appears in the content (case insensitive)
                movie_keywords = movie_name.lower().split()
                content_lower = content.lower()
                
                # Look for movie name or keywords in the content
                found_keywords = sum(1 for keyword in movie_keywords if keyword in content_lower)
                
                # If we find most of the keywords, consider it a match
                if found_keywords >= len(movie_keywords) * 0.5:  # At least 50% of keywords found
                    return True
                    
                # Also check for common movie-related indicators
                movie_indicators = ['download', 'watch', 'movie', 'film', 'hd', 'quality']
                indicator_count = sum(1 for indicator in movie_indicators if indicator in content_lower)
                
                if found_keywords > 0 and indicator_count > 0:
                    return True
                    
        return False
    except Exception as e:
        logger.warning(f"Error checking {url}: {str(e)}")
        return False

async def search_movie(movie_name: str) -> list:
    """Search for movie across all websites and return working links"""
    working_links = []
    
    # URL encode the movie name
    encoded_movie = quote(movie_name)
    
    # Create search URLs
    search_urls = [base_url + encoded_movie for base_url in MOVIE_SITES]
    
    # Use aiohttp for async requests
    async with aiohttp.ClientSession() as session:
        # Check all websites concurrently
        tasks = []
        for url in search_urls:
            task = check_website(session, url, movie_name)
            tasks.append((url, task))
        
        # Wait for all checks to complete
        for url, task in tasks:
            try:
                is_working = await task
                if is_working:
                    working_links.append(url)
                    logger.info(f"Found movie at: {url}")
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
    
    return working_links

async def handle_movie_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle movie search requests"""
    movie_name = update.message.text.strip()
    
    # Send "searching" message
    searching_msg = await update.message.reply_text(f"🔍 Searching for '{movie_name}' across movie websites...")
    
    try:
        # Search for the movie
        working_links = await search_movie(movie_name)
        
        if working_links:
            # Format the response with working links
            response = f"🎬 Found '{movie_name}' on {len(working_links)} website(s):\n\n"
            
            for i, link in enumerate(working_links, 1):
                # Extract website name from URL
                site_name = link.split('/')[2].replace('www.', '')
                response += f"{i}️⃣ {site_name}\n{link}\n\n"
            
            response += "📱 Click on the links above to visit the websites!\n"
            response += "⚠️ Note: Please ensure you're using these sites legally and safely."
            
        else:
            response = f"❌ Movie '{movie_name}' not found on any of the searched websites.\n\n"
            response += "💡 Try:\n"
            response += "• Checking the spelling\n"
            response += "• Using a different movie name\n"
            response += "• Trying the original/English title"
        
        # Edit the searching message with results
        await searching_msg.edit_text(response)
        
    except Exception as e:
        logger.error(f"Error in movie search: {str(e)}")
        await searching_msg.edit_text(
            f"❌ Sorry, there was an error searching for '{movie_name}'. Please try again later."
        )

def main() -> None:
    """Start the bot."""
    # Check if bot token is set
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: Please set your BOT_TOKEN in the code!")
        print("1. Go to @BotFather on Telegram")
        print("2. Create a new bot or use existing one")
        print("3. Copy the token and replace 'YOUR_BOT_TOKEN_HERE' in the code")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handle all text messages as movie search requests
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))

    # Run the bot until the user presses Ctrl-C
    print("🤖 Movie Search Bot is starting...")
    print("📱 Send /start to begin or just type a movie name!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()