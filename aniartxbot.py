from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Set up logging to debug errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7531426191:AAHZQqX6mVopST3-yh_IZpLtYRlaQ2k-fWA"

# Payment link
PAYMENT_LINK = "https://superprofile.bio/ps/65bb0868d3b539041fb8f334"

# Ownership footer
FOOTER = "Owned by ANIRUDH KARAMUNGIKAR (ARTIST) © 2025"

# Categories based on the provided HTML
CATEGORIES = {
    "Home": [],
    "Sketches": [],
    "Paintings": [],
    "Sculptures": [],
    "Customize": [
        "Accessories",
        "Shoes",
        "Shirts",
        "Phone Covers",
        "Skins",
        "Bags",
        "Kitchen Items",
        "Water Bottles"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = "Discover unique art at ANIRUDH ARTS GALLERY!\n\n" \
                     "Use /categories to explore our collections.\n\n" \
                     f"{FOOTER}"
    await update.message.reply_text(welcome_message)

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display main categories with an inline keyboard"""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f"cat_{category}")]
        for category in CATEGORIES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Choose a category:\n\n{FOOTER}",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks for categories and subcategories"""
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data.startswith("cat_"):
            category = data[4:]  # Extract category name
            if category == "Customize" and CATEGORIES[category]:
                # Show subcategories for Customize
                keyboard = [
                    [InlineKeyboardButton(subcat, callback_data=f"subcat_{subcat}")]
                    for subcat in CATEGORIES[category]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    f"Select a subcategory under {category}:\n\n{FOOTER}",
                    reply_markup=reply_markup
                )
            else:
                # Direct to payment for non-Customize categories
                await query.message.reply_text(
                    f"Explore {category}!\n"
                    f"Proceed to payment: {PAYMENT_LINK}\n\n"
                    f"After payment, send screenshot and target photo to +91 9860730275 or [email protected]\n\n"
                    f"{FOOTER}"
                )
        elif data.startswith("subcat_"):
            subcategory = data[7:]  # Extract subcategory name
            await query.message.reply_text(
                f"Explore {subcategory}!\n"
                f"Proceed to payment: {PAYMENT_LINK}\n\n"
                f"After payment, send screenshot and target photo to +91 9860730275 or [email protected].\n\n"
                f"{FOOTER}"
            )
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        await query.message.reply_text(
            f"Sorry, something went wrong. Please try again or contact support.\n\n{FOOTER}"
        )

def main():
    """Run the bot"""
    try:
        # Initialize the application with the bot token
        application = Application.builder().token(TOKEN).build()  