#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import datetime
import logging
import os
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv



load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

conn = sqlite3.connect('komandor.db', check_same_thread=False)
cursor = conn.cursor()


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [[
        InlineKeyboardButton("Добавить продажу", callback_data='1')

    ],
        [InlineKeyboardButton("получить данные за последний месяц ", callback_data='2'),
         InlineKeyboardButton("получить данные за год ", callback_data='3')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберете:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == '1':
        query.edit_message_text(text=f"Напиши  товар, номер покупателя и количество через запятую")
    if query.data == '2':
        cursor.execute(
            f"select count(distinct card_id), sum(checks) from sales where date between date(current_date, '-1 months') and date(current_date, '1 day')")
        records = cursor.fetchall()
        query.edit_message_text(
            text=f"За последний месяц было продано товаров  уникальным покупателям {records[0][0]} , в количестве {records[0][1]} руб")
    if query.data == '3':
        cursor.execute(
            f"select count(distinct card_id), sum(checks)  from sales where date between date(current_date, '-12 months') and date(current_date, '1 day')")
        records = cursor.fetchall()
        query.edit_message_text(
            text=f"За последние 12 месяцев было продано товаров  уникальным покупателям {records[0][0]} , в количестве  {records[0][1]} руб")


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Используйте  /start для запуска бота")


def add_base(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        amount, product, price = text.split(',')

        datet = str(datetime.datetime.now())
        data_b = (datet, amount, product, price)
        cursor.execute(f"INSERT INTO sales (date, lvl_5, card_id, checks) VALUES ( ?,?,?,?)", data_b)
        conn.commit()
        text = f" вы добавили запись дата : {datet}, количество : {amount}, товар : {product}, цена: {price} "
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    except:
        text = 'Вы ошиблись повторите, Напиши  количество, товар и цену через запятую'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    telegram_token = os.getenv('TELEGRAM_BOT')
    updater = Updater(telegram_token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), add_base))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
