import logging
import os

from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
