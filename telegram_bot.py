import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен вашего бота
TOKEN = "8099335643:AAHzpUjj7qZjCjRqdJx_8d0DPU_qT8ovfLA"

# Ссылки
LINKS = {
    "swap": "https://aerodrome.finance/swap?from=eth&to=0x5897040e2bdc84dd81bd7ee0e6edfdb4188b5790&chain0=8453&chain1=8453",
    "gecko": "https://www.geckoterminal.com/ru/base/pools/0x39a8ff1984f75a8b23db39e88d4800eb87aef2b5",
    "twitter": "https://x.com/BartMr82219",
    "website": "https://mrbartalameo.github.io/sparkcoin-site/",
    "basescan": "https://basescan.org/address/0x5897040e2bdc84dd81bd7ee0e6edfdb4188b5790"
}

# Тексты на разных языках
MESSAGES = {
    "en": {
        "welcome": "Welcome! Please choose your language:",
        "menu": "Choose an option:",
        "swap": "Buy SPRK",
        "gecko": "Gecko Terminal",
        "twitter": "Twitter",
        "website": "Our Website",
        "basescan": "Base Scan Contract",
        "lang_changed": "Language changed to English."
    },
    "de": {
        "welcome": "Willkommen! Bitte wählen Sie Ihre Sprache:",
        "menu": "Wählen Sie eine Option:",
        "swap": "SPRK kaufen",
        "gecko": "Gecko Terminal",
        "twitter": "Twitter",
        "website": "Unsere Website",
        "basescan": "Base Scan Vertrag",
        "lang_changed": "Sprache auf Deutsch geändert."
    },
    "es": {
        "welcome": "¡Bienvenido! Por favor, elige tu idioma:",
        "menu": "Elige una opción:",
        "swap": "Comprar SPRK",
        "gecko": "Gecko Terminal",
        "twitter": "Twitter",
        "website": "Nuestro sitio web",
        "basescan": "Contrato en Base Scan",
        "lang_changed": "Idioma cambiado a Español."
    },
    "fr": {
        "welcome": "Bienvenue ! Veuillez choisir votre langue :",
        "menu": "Choisissez une option :",
        "swap": "Acheter SPRK",
        "gecko": "Gecko Terminal",
        "twitter": "Twitter",
        "website": "Notre site web",
        "basescan": "Contrat Base Scan",
        "lang_changed": "Langue changée en Français."
    },
    "ru": {
        "welcome": "Добро пожаловать! Выберите язык:",
        "menu": "Выберите опцию:",
        "swap": "Купить SPRK",
        "gecko": "Gecko Terminal",
        "twitter": "Твиттер",
        "website": "Наш сайт",
        "basescan": "Контракт на Base Scan",
        "lang_changed": "Язык изменён на Русский."
    }
}

# Хранилище выбранных языков пользователей
user_languages = {}

# Клавиатура для выбора языка
def get_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en"),
         InlineKeyboardButton("Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("Español", callback_data="lang_es"),
         InlineKeyboardButton("Français", callback_data="lang_fr")],
        [InlineKeyboardButton("Русский", callback_data="lang_ru")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для основного меню
def get_main_menu(language):
    keyboard = [
        [InlineKeyboardButton(MESSAGES[language]["swap"], url=LINKS["swap"])],
        [InlineKeyboardButton(MESSAGES[language]["gecko"], url=LINKS["gecko"])],
        [InlineKeyboardButton(MESSAGES[language]["twitter"], url=LINKS["twitter"])],
        [InlineKeyboardButton(MESSAGES[language]["website"], url=LINKS["website"])],
        [InlineKeyboardButton(MESSAGES[language]["basescan"], url=LINKS["basescan"])]
    ]
    return InlineKeyboardMarkup(keyboard)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_languages:
        user_languages[user_id] = "en"  # Язык по умолчанию
    language = user_languages[user_id]
    await update.message.reply_text(
        MESSAGES[language]["welcome"],
        reply_markup=get_language_keyboard()
    )

# Обработчик выбора языка и меню
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data.startswith("lang_"):
        language = data.split("_")[1]
        user_languages[user_id] = language
        await query.message.reply_text(
            MESSAGES[language]["lang_changed"],
            reply_markup=get_main_menu(language)
        )
    else:
        language = user_languages.get(user_id, "en")
        await query.message.reply_text(
            MESSAGES[language]["menu"],
            reply_markup=get_main_menu(language)
        )

# Основная функция
async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Держим бота активным
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
