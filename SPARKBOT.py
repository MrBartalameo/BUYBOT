import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен от @BotFather
TOKEN = "8099335643:AAHzpUjj7qZjCjRqdJx_8d0DPU_qT8ovfLA"  # Проверь токен в @BotFather!

# Ссылки и данные
SPRK_POOL_URL = "https://www.geckoterminal.com/base/pools/0x39a8ff1984f75a8b23db39e88d4800eb87aef2b5"
SPRK_SWAP_URL = "https://aerodrome.finance/swap?from=eth&to=0x5897040e2bdc84dd81bd7ee0e6edfdb4188b5790&chain0=8453&chain1=8453"
SPRK_TWITTER_URL = "https://x.com/BartMr82219"

# Словари языков и переводов
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
        "en": "⚡ *SparkCoin* — AI-powered token on the Base chain.\n\nChoose an option below 👇",
        "ru": "⚡ *SparkCoin* — AI-токен на сети Base.\n\nВыберите действие 👇",
        "es": "⚡ *SparkCoin* — Token de IA en la red Base.\n\nElige una opción 👇",
        "de": "⚡ *SparkCoin* — KI-Token auf der Base-Chain.\n\nWähle eine Option 👇",
        "fr": "⚡ *SparkCoin* — Jeton IA sur Base.\n\nChoisissez une option 👇",
    },
}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
        for code, name in LANGUAGES.items()
    ]
    update.message.reply_text(
        translations["start"]["en"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def set_language(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    lang_code = query.data.replace("lang_", "")
    user_id = query.from_user.id
    user_languages[user_id] = lang_code

    keyboard = [
        [InlineKeyboardButton("🛒 Buy SPRK", url=SPRK_SWAP_URL)],
        [InlineKeyboardButton("📈 Price Chart", url=SPRK_POOL_URL)],
        [InlineKeyboardButton("📢 Twitter", url=SPRK_TWITTER_URL)],
    ]

    query.edit_message_text(
        text=translations["main_menu"][lang_code],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def main():
    logger.info("Запуск бота...")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))

    logger.info("Начало polling...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
