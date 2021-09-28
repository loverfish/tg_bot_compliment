import re
import random

from datetime import datetime as dt
from time import sleep


'''
создать словарь -> ключи: id пользователя, значение: переменная stop  
'''

stop = 0
compl_list = []


def form_a_list():
    new_list = []
    with open('compliment.txt') as f:
        for line in f:
            new_list.append(line.strip())
    return new_list


def form_a_txt():
    with open('compl_list.txt') as f:
        for line in f:
            global compl_list
            compl_list = re.split(r'\d+\. ', line)
            compl_list = list(filter(None, compl_list))

    with open('compliment.txt', 'w') as f:
        for elem in compl_list:
            f.write(elem.strip())
            f.write('\n')


def time_now_in_sec():
    time_now = dt.now().time()
    return time_now.hour * 3600 + time_now.minute * 60 + time_now.second


def min_now_in_sec():
    time_now = dt.now().time()
    return time_now.minute * 60 + time_now.second


def hourly_time_to_sleep():
    time_to_new_hour = 3600 - min_now_in_sec()
    return random.choice(range(time_to_new_hour, time_to_new_hour + 600))


def daily_time_to_sleep():
    time_to_new_day = 3600 * 24 - time_now_in_sec()
    return random.choice(range(time_to_new_day + 3600 * 9, time_to_new_day + 3600 * 11))


def interval_compliment(update, context, func):
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
        time_to_sleep = func()
        sleep(time_to_sleep)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry')


# form_a_txt()
compliment_list = form_a_list()
