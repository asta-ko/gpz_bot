#!/usr/bin/env python
# -*- coding: future_fstrings -*-
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from functools import wraps



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




LIST_OF_ADMINS = [12345678, 87654321]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped




# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def grant_access_to_user(username):
    pass    

def grant_access(bot, update, args=[]):
    if len(args):
        username = args[0]
        grant_access_to_user(username)
        update.message.reply_text("Вы дали доступ {0}".format(args[0]))
    else:
        update.message.reply_text("Попробуйте еще раз! Введите юзернейм после команды /grant_access")

def list_police_stations_available(bot, update):
    police_list = [{'number':78, 'detached_number':10, 'underaged':0, 'no_documents':3, 'medical_help_needed':1},
                   {'number':27, 'detached_number':6, 'underaged':1, 'no_documents':0, 'medical_help_needed':0}]
    police_short_list = [str(op.get('number')) for op in police_list]               
    if len(police_list):
        update.message.reply_text('На {0}: {1} задержанных в {2} отделах'.format('17:00', '123', '2'))
        for op in police_list:
            message_text = f"*{op.get('number')} ОП*\n _м. Маяковская, ул. Марата, 18_\n *{op.get('detached_number')} задержанных*"
            if op.get('underaged') or op.get('no_documents') or op.get('medical_help_needed'):
                message_text += ", из которых "
                if op.get('underaged'):
                    message_text += f"{op.get('underaged')} несовершеннолетних, "
                if op.get('no_documents'):
                    message_text += f"у {op.get('no_documents')} нет при себе документов, "
                if op.get('medical_help_needed'):
                    message_text += f"{op.get('medical_help_needed')} нужна медицинская помощь, "
                message_text = message_text[0:-2]

            update.message.reply_text(text=message_text, parse_mode=telegram.ParseMode.MARKDOWN)

        custom_keyboard = [[InlineKeyboardButton(x+'ОП', callback_data=x) for x in police_short_list]]#[police_short_list]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text="Куда поедем?", reply_markup=reply_markup)

    else:
        update.message.reply_text("На данный момент нет информации о задержанных.")


def op_button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Отлично. Поедем в {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)



# def echo(bot, update):
#     """Echo the user message."""
#     user = update.effective_user 
#     logger.info((bot, user.id, user.first_name, user.last_name, 'USER'))
#     update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("678222224:AAGv2STf-5GCwy31KBbVoiwQnXp_nALPH8g")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("grant_access", grant_access, pass_args=True))
    dp.add_handler(CommandHandler("list_op", list_police_stations_available))
    dp.add_handler(CallbackQueryHandler(op_button))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()