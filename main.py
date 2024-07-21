import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from datetime import datetime, timedelta
import random
import asyncio

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Ваш API ключ бота от BotFather
API_KEY = '6617156148:AAGnfhsSv7bZ6PL2fglaESrUeEC3ZZ6FfLc'
CHAT_ID = '1445675314'

# Список приятных слов
nice_words = [
    "Ты самая лучшая мама на свете!",
    "Спасибо тебе за всё!",
    "Я тебя люблю!",
    "Ты прекрасна!",
    "Ты всегда поддерживаешь меня!"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    CHAT_ID = update.message.chat_id
    """Запускает бота и планировщик сообщений."""
    await update.message.reply_text('Бот запущен и будет отправлять приятные слова каждый час!')

    current_time = datetime.now()

    while current_time.minute != 16:
        await asyncio.sleep(60)
        current_time = datetime.now()

    # Начать отправку сообщений каждый час
    asyncio.create_task(send_nice_words_every_hour(context))


async def send_nice_words(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет случайное приятное слово."""
    word = random.choice(nice_words)
    await context.bot.send_message(chat_id=CHAT_ID, text=word)

async def send_nice_words_every_hour(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запускает бесконечный цикл отправки сообщений каждый час."""
    while True:
        await send_nice_words(context)
        await asyncio.sleep(60)  # Ждать 1 час

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображает информацию о том, как использовать бота."""
    await update.message.reply_text("Используйте /start для запуска бота.")

def main() -> None:
    """Запуск бота."""
    application = (
        Application.builder()
        .token(API_KEY)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Запуск бота до нажатия Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
