import logging
import os
from bot_requests import *

from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['/help'], ['/groups'], ['Скрыть']])
    await update.message.reply_text(text='Чем могу помочь?', reply_markup=keyboard)


async def on_message(update, context: CallbackContext):
    text = update.message.text
    if text == 'Скрыть':
        await update.message.reply_text(text='Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())
    elif text == 'Назад':
        await on_start(update, context)


async def help(update, context):
    file = open("description/help.txt", 'r', encoding='utf-8')
    message = str(file.read())
    await update.message.reply_text(message)


async def list_of_groups(update, context):
    keyboard = ReplyKeyboardMarkup([['/return'], []])
    strings = [f"{group['id']}. {group['name']}" for group in get_list_of_groups()["groups"]]
    strings.append('Напишите id нужной группы вопросов')
    await update.message.reply_text('\n'.join(strings), reply_markup=keyboard)
    return 1


async def get_id(update, context):
    text = update.message.text
    await update.message.reply_text('123123')
    # if text in [str(group['id']) for group in get_list_of_groups()["groups"]]:
    #     context.user_data["group_id"] = text
    #     context.user_data["questions"] = get_list_of_questions(text)
    #     context.user_data["current"] = 0
    #     await update.message.reply_text(f"Выбрана группа вопросов: {get_group(text)['name']}.")
    #     return 2
    # else:
    #     await update.message.reply_text('Группы с таким id не существует.')


async def question_response(update, context):
    pass


async def answer_response(update, context):
    pass


async def end_dialog(update, context):
    keyboard = ReplyKeyboardMarkup([['/help'], ['/groups'], ['Скрыть']])
    await update.message.reply_text('Группа вопросов завершена',
                                    reply_markup=keyboard)
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", help))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('groups', list_of_groups)],
        states={
            1: [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=get_id)],
            2: [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=end_dialog)]
        },

        fallbacks=[CommandHandler('return', end_dialog)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
