import logging
import os
from bot_requests import *

from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['/help'], ['/groups'], ['/site']])
    await update.message.reply_text(text='Чем могу помочь?', reply_markup=keyboard)


async def site(update, context):
    await update.message.reply_text(URL)


async def help(update, context):
    file = open("description/help.txt", 'r', encoding='utf-8')
    message = str(file.read())
    await update.message.reply_text(message)


async def list_of_groups(update, context):
    keyboard = ReplyKeyboardMarkup([['/return'], []])
    strings = [f"{group['id']}. {group['name']}" for group in get_list_of_groups()]
    if strings:
        strings.append('Напишите id нужной группы вопросов')
    else:
        strings.append(f'Нет доступных групп для повторения. Добавьте их на сайте {URL}')
        keyboard = ReplyKeyboardMarkup([['/help'], ['/groups'], ['/site']])
        await update.message.reply_text('\n'.join(strings), reply_markup=keyboard)
        return ConversationHandler.END
    await update.message.reply_text('\n'.join(strings), reply_markup=keyboard)
    return 1


async def get_id(update, context):
    text = update.message.text
    if text in [str(group['id']) for group in get_list_of_groups()]:
        context.user_data["questions"] = [get_question(int(i)) for i in get_group(int(text))["questions"]]
        context.user_data["last"] = len(context.user_data["questions"]) - 1
        context.user_data["current"] = 0
        question = context.user_data["questions"][context.user_data["current"]]["question"]
        await update.message.reply_text(f"Выбрана группа вопросов: {get_group(text)['group']['name']}.")
        await update.message.reply_text(' '.join(['Вопрос:', question]))
        return 2
    else:
        await update.message.reply_text('Группы с таким id не существует.')


async def reply_response(update, context):
    keyboard = ReplyKeyboardMarkup([['/help'], ['/groups'], ['/site']])
    answer = context.user_data["questions"][context.user_data["current"]]["answer"]
    question = context.user_data["questions"][context.user_data["current"]]["question"]
    await update.message.reply_text(' '.join(["Ответ:", answer]))
    if context.user_data['current'] < context.user_data['last']:
        context.user_data['current'] += 1
        await update.message.reply_text(' '.join(["Вопрос:", question]))
        return 2
    else:
        await update.message.reply_text('Группа вопросов завершена', reply_markup=keyboard)
        return ConversationHandler.END


async def end_dialog(update, context):
    keyboard = ReplyKeyboardMarkup([['/help'], ['/groups']])
    await update.message.reply_text('Группа вопросов завершена',
                                    reply_markup=keyboard)
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("site", site))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('groups', list_of_groups)],
        states={
            1: [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=get_id)],
            2: [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=reply_response)],
            3: [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=reply_response)]
        },

        fallbacks=[CommandHandler('return', end_dialog)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
