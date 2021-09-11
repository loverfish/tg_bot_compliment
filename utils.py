import re

from datetime import datetime as dt


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
    print(time_now)
    return time_now.hour * 3600 + time_now.minute * 60 + time_now.second


def min_now_in_sec():
    time_now = dt.now().time()
    return time_now.minute * 60 + time_now.second


# form_a_txt()
compliment_list = form_a_list()
