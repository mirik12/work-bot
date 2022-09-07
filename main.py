import json
import time
from datetime import timedelta, datetime
import random
from datetime import datetime

import now as now
import telebot
from telebot import types
from main_db import *
from dataclasses import *
from main_db_test import *
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import re
from threading import Thread

#
bot = telebot.TeleBot('5345239769:AAGMA-jXu2iFkHkJ0D5HKlzVnva-zXzXYik')
my_dict = {}
# --------  1. Сделать инлайны кннопки для выбрать месяц + сделать так чтобы выбранный месяц писался от бота (кконкертный месяц)"!!!!!!!!!!!!!!!!!!!!
# 2. как мы будем получать статистику за конкретный месяц + попробовать написать конкретный код

# buttonsа
add_time_text = 'Добавить часы'
statistics_time_month_text = 'Статистика за месяц'
instruction_text = 'Инструкция'
settings_text = 'Настройки'
settings_yes_text = 'Да'
settings_no_text = 'Нет'
no_command_text = 'Я не знаю такой функции'

# return to main menu
return_to_main_menu_text = 'Главное меню'

# buttons into function
statistics_this_month_text = 'Текущий месяц'
statistics_select_month_text = 'Выбрать месяц'
add_how_much_time_text = 'Во сколько ты начал сегодня работать?'
settings_push_text = 'Настройка push уведомлений'
settings_push_question_text = 'Присылать ли Вам напоминание о добавлениии часов?'
push_yes_text = 'Да'
push_no_text = 'Нет'
return_one_step_text = 'Назад'

# text
instruction_into_button_text = 'После команды "start" у Вас появляется главное меню, в котором....'

btn_return_menu = types.KeyboardButton(return_to_main_menu_text)
btn_return_one_step = types.KeyboardButton(return_one_step_text)

#TODO выучить все о потоках
#TODO какк вместо 64 и 65 сделать одной строкой , вызываю один метод . *вызывать один метод 63,64,65 , то есть чтобы в принципе у DBhelper вызывался один метод


push_thread = Thread()
@bot.message_handler(commands=['start'])
def start(message):

    # mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    # bot.send_message(message.chat.id, mess, parse_mode='html')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # website = types.KeyboardButton.('')

    text = f"Привет {message.from_user.first_name} {message.from_user.last_name}"
    show_main_menu_func(message, text)
    dbhelper = DBHelper()
    # dbhelper.create_table()
    # dbhelper.create_table_for_push()
    # dbhelper.add_to_create_table_for_push(message.chat.id, True)
    # dbhelper.create_table().create_table_for_push().add_to_create_table_for_push(message.chat.id, True)
    dbhelper.all_in_one_create_tables(message.chat.id)
    push_thread = Thread(target=start_push_cycle(message), args=())
    push_thread.start()
    # a1 = th.is_alive()
    # a2 = th.isAlive()
    # print(a1)
    # print(a2)



@bot.message_handler(content_types=['text'])
def detected_user_tap(message):
    if message.text == add_time_text:
        add_start_time_func(message)

    elif message.text == 'Статистика':
        statistics_time_func(message)
    elif message.text == instruction_text:
        instruction_func(message)
    elif message.text == settings_text:
        settings_func(message)

    elif message.text == statistics_this_month_text:
        add_to_dict('month', datetime.now().date().month)
        this_month(message)
    elif message.text == statistics_select_month_text:
        list_of_months_func(message)

        # statistics_per_month_func(message)
    elif message.text == return_to_main_menu_text:
        return_to_main_menu_func(message)

    elif message.text == add_how_much_time_text:
        add_start_time_func(message)

    # elif message.text == settings_push_text:
    #     settings_push_func(message)

    elif message.text == 'Время начала':
        add_start_time_func(message)

    elif message.text == 'Время конца':
        add_end_time_func(message)

    elif message.text == 'Отмена':
        calculate_work_time(message)
    

    elif message.text == 'Редактировать':
        edit_menu_func(message)

    elif message.text == 'Дату':
        edit_date(message)


    # регулярные выражения
    elif re.match('\d\d/\d\d/\d{4}', message.text):
        add_to_dict('date', message.text)
        calculate_work_time(message)


    elif message.text == 'Принять':
        dbhelper = DBHelper()
        today_result = dbhelper.data_check(my_dict['date'])
        if today_result:
            bot.send_message(message.chat.id, text='Эта дата уже есть , чтобы изменить дату нажмите редактировать и выберите "дату"')
        else:
            add_to_data_base(message)
            accept_mes_plus_return_to_menu(message)


    # elif message.text == 'Радактировать':
    #     start(message)

    # Вывести сообщение что сохранено и перейти в меню

    # elif message.text == '8:00':
    #     time_8_func(message)
    else:
        no_command_func(message)


# @bot.message_handler(text=['Редактировать'])
# def start(message):
#     calendar, step = DetailedTelegramCalendar().build()
#     bot.send_message(message.chat.id, text='Редактировать'
#                      f"Select {LSTEP[step]}",
#                      reply_markup=calendar)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         bot.edit_message_text(f"Select {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"You selected {result}",
#                               c.message.chat.id,
#                               c.message.message_id)

# TODO оооооо



def show_main_menu_func(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add_time = types.KeyboardButton(add_time_text)
    btn_statistics_time = types.KeyboardButton('Статистика')
    btn_instruction = types.KeyboardButton(instruction_text)
    btn_settings = types.KeyboardButton(settings_text)
    markup.add(btn_add_time, btn_statistics_time)
    markup.row(btn_instruction, btn_settings)
    bot.send_message(message.chat.id,
                     text=text.format(message.from_user), reply_markup=markup)



def accept_mes_plus_return_to_menu(message):
    bot.send_message(message.chat.id, text='Данные успешно сохранены')
    return_to_main_menu_func(message)


def add_start_time_func(message):
    add_to_dict('date', str(get_date_today()))
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    time_6_7_btn = types.InlineKeyboardButton(text='6-7', callback_data='s_hours:06')
    time_7_8_btn = types.InlineKeyboardButton(text='7-8', callback_data='s_hours:07')
    time_8_9_btn = types.InlineKeyboardButton(text='8-9', callback_data='s_hours:08')
    time_9_10_btn = types.InlineKeyboardButton(text='9-10', callback_data='s_hours:09')
    time_10_11_btn = types.InlineKeyboardButton(text='10-11', callback_data='s_hours:10')
    time_11_12_btn = types.InlineKeyboardButton(text='11-12', callback_data='s_hours:11')
    markup_inline.add(time_6_7_btn, time_7_8_btn, time_8_9_btn, time_9_10_btn, time_10_11_btn, time_11_12_btn)
    bot.send_message(message.chat.id, text=add_how_much_time_text, reply_markup=markup_inline)


def time_quaters_minutes_func(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    start_hour = my_dict['s_hours']
    time_00_btn = types.InlineKeyboardButton(text=start_hour + ':00', callback_data='s_minutes:00')
    time_15_btn = types.InlineKeyboardButton(text=start_hour + ':15', callback_data='s_minutes:15')
    time_30_btn = types.InlineKeyboardButton(text=start_hour + ':30', callback_data='s_minutes:30')
    time_45_btn = types.InlineKeyboardButton(text=start_hour + ':45', callback_data='s_minutes:45')
    markup_inline.add(time_00_btn, time_15_btn, time_30_btn, time_45_btn)
    bot.send_message(message.chat.id, text='Вы начали работать в ', reply_markup=markup_inline)


def add_end_time_func(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    time_15_16_btn = types.InlineKeyboardButton(text='15-16', callback_data='end_hours:15')
    time_16_17_btn = types.InlineKeyboardButton(text='16-17', callback_data='end_hours:16')
    time_17_18_btn = types.InlineKeyboardButton(text='17-18', callback_data='end_hours:17')
    time_18_19_btn = types.InlineKeyboardButton(text='18-19', callback_data='end_hours:18')
    time_19_20_btn = types.InlineKeyboardButton(text='19-20', callback_data='end_hours:19')
    time_20_21_btn = types.InlineKeyboardButton(text='20-21', callback_data='end_hours:20')
    markup_inline.add(time_15_16_btn, time_16_17_btn, time_17_18_btn, time_18_19_btn, time_19_20_btn, time_20_21_btn)
    bot.send_message(message.chat.id, text='Во сколько Вы закончили работать', reply_markup=markup_inline)


def list_of_months_func(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=3)
    month_1 = types.InlineKeyboardButton(text='Январь', callback_data='month:01')
    month_2 = types.InlineKeyboardButton(text='Февраль', callback_data='month:02')
    month_3 = types.InlineKeyboardButton(text='Март', callback_data='month:03')
    month_4 = types.InlineKeyboardButton(text='Апрель', callback_data='month:04')
    month_5 = types.InlineKeyboardButton(text='Май', callback_data='month:05')
    month_6 = types.InlineKeyboardButton(text='Июнь', callback_data='month:06')
    month_7 = types.InlineKeyboardButton(text='Июль', callback_data='month:07')
    month_8 = types.InlineKeyboardButton(text='Август', callback_data='month:08')
    month_9 = types.InlineKeyboardButton(text='Сентябрь', callback_data='month:09')
    month_10 = types.InlineKeyboardButton(text='Октябрь', callback_data='month:10')
    month_11 = types.InlineKeyboardButton(text='Ноябрь', callback_data='month:11')
    month_12 = types.InlineKeyboardButton(text='Декабрь', callback_data='month:12')
    markup_inline.add(month_1, month_2, month_3, month_4, month_5, month_6, month_7, month_8, month_9, month_10, month_11, month_12)
    bot.send_message(message.chat.id, text='Выберите месяц за который Вы хотите получить статистику', reply_markup=markup_inline)


def select_month(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)

def time_quaters_minutes_end_func(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    end_hours = my_dict['end_hours']
    time_00_btn = types.InlineKeyboardButton(text=end_hours + ':00', callback_data='end_minutes:00')
    time_15_btn = types.InlineKeyboardButton(text=end_hours + ':15', callback_data='end_minutes:15')
    time_30_btn = types.InlineKeyboardButton(text=end_hours + ':30', callback_data='end_minutes:30')
    time_45_btn = types.InlineKeyboardButton(text=end_hours + ':45', callback_data='end_minutes:45')
    markup_inline.add(time_00_btn, time_15_btn, time_30_btn, time_45_btn)
    bot.send_message(message.chat.id, text='Вы закончили работать в ', reply_markup=markup_inline)

#####------###
def calculate_work_time(message):
    sum_work_hour = get_hours_sum()
    message_text = 'Время начала: ' + get_start_time() + \
                   '\nВремя конца: ' + get_end_time() + \
                   '\nДата: ' + my_dict['date'] + \
                   '\n\nВы проработали: ' + sum_work_hour.hours_minutes_text()
    # '\n\nВы проработали: ' + str(sum_work_hour.hour) + ' часов ' + str(sum_work_hour.minute) + ' минут '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    accept_btn = types.KeyboardButton(text='Принять')
    edit_btn = types.KeyboardButton(text='Редактировать')
    markup.add(accept_btn, edit_btn, btn_return_menu)
    bot.send_message(message.chat.id, text=message_text, reply_markup=markup)



def edit_menu_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    edit_start_time = types.KeyboardButton(text='Время начала')
    edit_end_time = types.KeyboardButton(text='Время конца')
    edit_date_time = types.KeyboardButton(text='Дату')
    btn_cancel = types.KeyboardButton(text='Отмена')
    markup.add(edit_start_time, edit_end_time, edit_date_time, btn_cancel, btn_return_menu)
    bot.send_message(message.chat.id, text='Что Вы хотите редактировать?', reply_markup=markup)




def edit_date(message):
    bot.send_message(message.chat.id,
                     text='Переключитесь на клавиатуру и введите дату в формате ДАТА/МЕСЯЦ/ГОД (12/03/1996)')


def add_to_data_base(message):
    dbhelper = DBHelper()
    # id = message.from_user.id
    id = message.chat.id
    date = my_dict['date']
    # start_time = to_string_from_dict('s_hours') + ':' + to_string_from_dict('s_minutes')
    # end_time = to_string_from_dict('end_hours') + ':' + to_string_from_dict('end_minutes')
    dbhelper.create_add_to_table(id, date, get_start_time(), get_end_time(), get_hours_sum().get_time_string())



def this_month(message):
    dbhelper = DBHelper()
    month = to_int_from_dict('month')
    statistics_list = dbhelper.get_statistics_from_table(message.chat.id, month)
    if len(statistics_list) == 0:
        bot.send_message(message.chat.id, text='В выбранном месяце нет записей о работе')
    else:
        working_hours = get_statistics_working_hours(statistics_list)  # message.from_user.id
        text = get_statistics_string(statistics_list, working_hours)
        bot.send_message(message.chat.id, text=text)
    # today = datetime.today()
    # datem = datetime(today.year, today.month, 1)
    # return datem.month

def get_start_time():
    return to_string_from_dict('s_hours') + ':' + to_string_from_dict('s_minutes')


def get_end_time():
    return to_string_from_dict('end_hours') + ':' + to_string_from_dict('end_minutes')


def get_hours_sum():
    # start_time_1 = datetime.now()
    # start_time_1.hour = to_int_from_dict('s_hours')
    # start_time_1.minute = to_int_from_dict('s_minutes')
    # date = datetime.time(to_int_from_dict('s_hours'), to_int_from_dict('s_minutes'))
    # start_time = MyTime(hours=to_int_from_dict('s_hours'), minutes=to_int_from_dict('s_minutes'))
    # end_time = MyTime(hours=to_int_from_dict('end_hours'), minutes=to_int_from_dict('end_minutes'))
    # result_time = datetime.fromtimestamp((end_time - start_time).total_seconds())
    # print(result_time.hour, result_time.minute)
    # return result_time

    start_time = MyTime(hours=to_int_from_dict('s_hours'), minutes=to_int_from_dict('s_minutes'))
    end_time = MyTime(hours=to_int_from_dict('end_hours'), minutes=to_int_from_dict('end_minutes'))
    result_time = get_working_hours(start_time, end_time)
    print(result_time.hours, result_time.minutes)
    return result_time


def get_date_today():
    current_datetime = datetime.now().date()
    dd_mm_YYYY = current_datetime.strftime('%d/%m/%Y')
    return dd_mm_YYYY


def add_to_dict(key, value):
    my_dict[key] = value


# callback = s = key:value
#push:False
def split_callback_and_return_key(callback: str):
    callback_pair = callback.split(':')
    add_to_dict(callback_pair[0], callback_pair[1])
    print(my_dict)
    return callback_pair[0]


# def object_to_json(my_object):
#     res = json.dumps(my_object, cls=MyEncoder)
#     print('json: '+res)


@bot.callback_query_handler(func=lambda call: True)
def answer(callback: types.CallbackQuery):
    key = split_callback_and_return_key(callback.data)
    if key == 's_hours':
        time_quaters_minutes_func(callback.message)
    elif key == 's_minutes':
        add_end_time_func(callback.message)
    elif key == 'end_hours':
        time_quaters_minutes_end_func(callback.message)
    elif key == 'end_minutes':
        calculate_work_time(callback.message)
    elif key == 'month':
        bot.send_message(callback.message.chat.id, text = 'Вы выбрали '+  month_name(to_int_from_dict('month')) + ' месяц')
        this_month(callback.message)
      #push:False
      #'end_minutes:45'
    elif key == 'push':
        switch_push_status(callback.message)
        bot.send_message(callback.message.chat.id, text="Статус изменен")
        return_to_main_menu_func(callback.message)
    else:
        bot.send_message(callback.message.chat.id, text='Неверный ключ' + key,
                         reply_markup=callback.message.reply_markup)

#     if to_string_from_dict(month) ==  1
    # if call.data == '8':
    #     time_quaters_minutes_func(call.message, '8')
    # elif call.data == '9':
    #     time_quaters_minutes_func(call.message, '9')
    # elif call.data == '10':
    #     time_quaters_minutes_func(call.message, '10')
    # else:
    #     bot.send_message(call.message.chat.id, text='Выберите другое время', reply_markup=call.message.reply_markup)


def statistics_time_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_statistics_per_week = types.KeyboardButton(statistics_this_month_text)
    btn_statistics_per_text = types.KeyboardButton(statistics_select_month_text)
    markup.add(statistics_this_month_text, statistics_select_month_text, btn_return_menu)
    bot.send_message(message.chat.id, text='Статистика по рабочим часам. Выберите период', reply_markup=markup)


def instruction_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_return_menu)
    bot.send_message(message.chat.id, text=instruction_into_button_text, reply_markup=markup)

#TODO проверить статус пушшей юзера ПЕРЕДЕЛАТЬ НА Inline кнопки
def settings_func(message):
    # тут получим юзера( статус пушей юзера)
    result = DBHelper().get_push_status(message.chat.id)
    bot_message = ''
    push_btn_text = ''
    push_btn_callback = 'push:'
    if result:
        bot_message = 'Включено'
        push_btn_callback += str(not result)
        push_btn_text = 'Выключить'
    else:
        bot_message = 'Выключено'
        push_btn_callback += str(not result)
        push_btn_text = 'Включить'
    print(push_btn_callback)
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    btn_settings_push = types.InlineKeyboardButton(text=push_btn_text, callback_data=push_btn_callback)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn_settings_push = types.KeyboardButton(push_btn_text)
    # markup.add(btn_return_menu, btn_settings_push)
    markup_inline.add(btn_settings_push)
    bot.send_message(message.chat.id, text='Текущий статус: ' + bot_message, reply_markup=markup_inline)

    #callback = push:False
def switch_push_status(message):
    DBHelper().update_user_push_status(message.chat.id, to_bool_from_dict('push'))



def start_push_cycle(message):
    # Запускаем цикл для проверки времени
    while push_thread.is_alive():
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time == '20:00':  # Выставляете ваше время
            print('pass')
            bot.send_message(message.chat.id, text="заполни время")

        else:
            print('no push')
        time.sleep(60)


# def settings_push_func(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_push_yes = types.KeyboardButton(push_yes_text)
#     btn_push_no = types.KeyboardButton(push_no_text)
#     markup.add(btn_push_yes, btn_push_no, btn_return_one_step)
#     bot.send_message(message.chat.id, text=settings_push_question_text, reply_markup=markup)


def no_command_func(message):
    bot.send_message(message.chat.id, text=no_command_text)


def statistics_per_month_func(message):
    bot.send_message(message.chat.id, text=statistics_time_month_text)


def return_to_main_menu_func(message):
    show_main_menu_func(message, return_to_main_menu_text)


def to_string_from_dict(key):
    int_value = my_dict[key]
    return str(int_value)


def to_int_from_dict(key):
    value = my_dict[key]
    return int(value)

def to_bool_from_dict(key):
    value = my_dict[key]
    return value.lower() in ['true']


# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     if message.text == 'Hello':
#         bot.send_message(message.chat.id, 'и тебе привет', parse_mode='html')
#     elif message.text == 'id':
#         bot.send_message(message.chat.id, f'твой id: {message.from_user.id}', parse_mode='html')
#     elif message.text == 'photo':
#         photo = open('1_E5Dd_j3Ldg6kYKXEXjFMpg.jpeg', 'rb')
#         bot.send_photo(message.chat.id, photo)
#     else:
#         bot.send_message(message.chat.id, 'я тебя не понимаю', parse_mode='html')

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау Крутое фото')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посетить веб сайт', url='https://eurosport.com'))
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    website = types.KeyboardButton('Вэб сайт')
    start = types.KeyboardButton('Start')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


bot.polling(none_stop=True)
