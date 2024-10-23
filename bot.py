import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_API_TOKEN' with the token you got from BotFather
API_TOKEN = '7894297267:AAH94kogQ8AigxZSk7nuMgeLRbLWf2G4EdM'

# Predefined static affiliate links for different categories
affiliate_links = {
    "electronics": [
        {"name": "Smartphone Deals", "url": "https://www.jumia.com/smartphones-affiliate-link"},
        {"name": "Laptop Offers", "url": "https://www.jumia.com/laptops-affiliate-link"},
        {"name": "TVs & Accessories", "url": "https://www.jumia.com/tvs-affiliate-link"}
    ],
    "fashion": [
        {"name": "Men's Fashion", "url": "https://www.jumia.com/mens-fashion-affiliate-link"},
        {"name": "Women's Fashion", "url": "https://www.jumia.com/womens-fashion-affiliate-link"},
        {"name": "Shoes & Accessories", "url": "https://www.jumia.com/shoes-affiliate-link"}
    ],
    "home": [
        {"name": "Kitchen Appliances", "url": "https://www.jumia.com/kitchen-affiliate-link"},
        {"name": "Home Furniture", "url": "https://www.jumia.com/furniture-affiliate-link"},
        {"name": "Cleaning Supplies", "url": "https://www.jumia.com/cleaning-affiliate-link"}
    ]
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create inline button for "Explore Deals"
    keyboard = [[InlineKeyboardButton("Explore Deals", callback_data='explore_deals')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send welcome message with "Explore Deals" button
    await update.message.reply_text(
        "Welcome to JumiaDealsBot! Click the button below to explore categories.",
        reply_markup=reply_markup
    )

# Explore deals handler - show category buttons
async def explore_deals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Create buttons for categories
    keyboard = [
        [InlineKeyboardButton("Electronics", callback_data='electronics')],
        [InlineKeyboardButton("Fashion", callback_data='fashion')],
        [InlineKeyboardButton("Home", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Show category options
    await query.edit_message_text("Select a category:", reply_markup=reply_markup)

# Category selection handler
async def category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    category = query.data
    if category in affiliate_links:
        # Create inline buttons for affiliate links in the selected category
        keyboard = [
            [InlineKeyboardButton(item["name"], url=item["url"])]
            for item in affiliate_links[category]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Show deals for the selected category
        await query.edit_message_text(f"Here are some {category.capitalize()} deals from Jumia:", reply_markup=reply_markup)

# Main function to start the bot
def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Add handlers for commands and callbacks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(explore_deals, pattern='explore_deals'))
    application.add_handler(CallbackQueryHandler(category_selection, pattern='^(electronics|fashion|home)$'))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()
