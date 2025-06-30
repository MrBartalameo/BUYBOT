import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8099335643:AAHzpUjj7qZjCjRqdJx_8d0DPU_qT8ovfLA"  # Проверь токен в @BotFather!

SPRK_TOKEN_ADDRESS = "0x5897040e2bdC84Dd81Bd7eE0E6edFdB4188B5790"
SPRK_POOL_URL = "https://www.geckoterminal.com/base/pools/0x39a8ff1984f75a8b23db39e88d4800eb87aef2b5"
SPRK_SWAP_URL = f"https://aerodrome.finance/swap?from=eth&to=0x5897040e2bdc84dd81bd7ee0e6edfdb4188b5790&chain0=8453&chain1=8453"
SPRK_TWITTER_URL = "https://x.com/BartMr82219"

LANGUAGES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "es": "🇪🇸 Español",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
}

user_languages = {}

translations = {
    "start": {
        "en": "Welcome to SparkCoin! Choose your language:",
        "ru": "Добро пожаловать в SparkCoin! Выберите язык:",
        "es": "¡Bienvenido a SparkCoin! Elige tu idioma:",
        "de": "Willkommen bei SparkCoin! Wähle deine Sprache:",
        "fr": "Bienvenue sur SparkCoin ! Choisissez votre langue :",
    },
    "main_menu": {
        "en": "⚡ *SparkCoin* — AI-powered token on the Base chain.\n\n💰 *Price*: ${price}\n📊 *Volume 24h*: ${volume}\n\nChoose an option below 👇",
        "ru": "⚡ *SparkCoin* — AI-токен на сети Base.\n\n💰 *Цена*: ${price}\n📊 *Объём за 24ч*: ${volume}\n\nВыберите действие 👇",
        "es": "⚡ *SparkCoin* — Token de IA en la red Base.\n\n💰 *Precio*: ${price}\n📊 *Volumen 24h*: ${volume}\n\nElige una opción 👇",
        "de": "⚡ *SparkCoin* — KI-Token auf der Base-Chain.\n\n💰 *Preis*: ${price}\n📊 *Volumen 24h*: ${volume}\n\nWähle eine Option 👇",
        "fr": "⚡ *SparkCoin* — Jeton IA sur Base.\n\n💰 *Prix*: ${price}\n📊 *Volume 24h*: ${volume}\n\nChoisissez une option 👇",
    },
}

def get_sprk_stats():
    try:
        url = "https://api.geckoterminal.com/api/v2/networks/base/pools/0x39a8ff1984f75a8b23db39e88d4800eb87aef2b5"
        response = requests.get(url).json()
        price = float(response["data"]["attributes"]["base_token_price_usd"])
        volume = float(response["data"]["attributes"]["volume_usd"]["h24"])
        return round(price, 6), int(volume)
    except Exception as e:
        logger.error(f"Error fetching SPRK stats: {e}")
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
        for code, name in LANGUAGES.items()
    ]
    await update.message.reply_text(
        translations["start"]["en"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()

    lang_code = query.data.replace("lang_", "")
    user_id = query.from_user.id
    user_languages[user_id] = lang_code

    price, volume = get_sprk_stats()
    if price is None:
        await query.edit_message_text("❌ Failed to get token data. Try again later.")
        return

    text = translations["main_menu"][lang_code].replace("${price}", str(price)).replace("${volume}", str(volume))

    keyboard = [
        [InlineKeyboardButton("🛒 Buy SPRK", url=SPRK_SWAP_URL)],
        [InlineKeyboardButton("📈 Price Chart", url=SPRK_POOL_URL)],
        [InlineKeyboardButton("📢 Twitter", url=SPRK_TWITTER_URL)],
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def main():
    logger.info("Запуск бота...")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))

    logger.info("Начало polling...")
    application.run_polling()

if __name__ == "__main__":
    main()