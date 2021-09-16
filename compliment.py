
import logging
import random

from threading import Thread

from time import sleep

from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup

from setup_list import bot_compliment_tg_token
from utils import compliment_list, hourly_time_to_sleep, interval_compliment


updater = Updater(token=bot_compliment_tg_token)
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm the compliment bot, please talk to me!",
        reply_markup=markup)


def single_compliment(update, context):
    # message = random.choice(result_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=random.choice(compliment_list))


def daily_compliment(update, context):
    global stop
    stop = None
    flexible_list = compliment_list.copy()
    while flexible_list:
        if stop:
            break
        message = random.choice(flexible_list)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{message}')
        flexible_list.remove(message)
        if not flexible_list:
            flexible_list = compliment_list.copy()
        time_to_sleep = 3600
        # sleep(random.choice(range(time_to_sleep, time_to_sleep + 900)))
        random_time = random.choice(range(time_to_sleep, time_to_sleep + 240))
        sleep(random_time)
        # sleep(3600)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry')


def hourly_compliment(update, context):
    time_to_sleep = hourly_time_to_sleep()
    interval_compliment(update, context, time_to_sleep)


def stop_compliment(update, context):
    global stop
    stop = True
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Stop daily compliments\n'
                                  'For correct operation do not run "daily compliment" for 27 hours')


def compliment_stream(update, context):
    Thread(target=daily_compliment, args=(update, context)).start()


def hourly_compliment_stream(update, context):
    Thread(target=hourly_compliment, args=(update, context)).start()


reply_keyboard = [['/more', '/daily']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


start_handler = CommandHandler('start', start)
single_compliment_handler = CommandHandler('more', single_compliment)
daily_compliment_handler = CommandHandler('daily', compliment_stream)
hourly_compliment_handler = CommandHandler('hourly', hourly_compliment_stream)
stop_handler = CommandHandler('stop', stop_compliment)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(single_compliment_handler)
dispatcher.add_handler(daily_compliment_handler)
dispatcher.add_handler(hourly_compliment_handler)
dispatcher.add_handler(stop_handler)

updater.start_polling()
updater.idle()
