import json

import telebot
from telebot import types
from dataclasses import *

bot = telebot.TeleBot('5345239769:AAGMA-jXu2iFkHkJ0D5HKlzVnva-zXzXYik')
my_dict = {}
#--------  1. Cделать так чтобы строка 111 превращалась в ключ значение и сохранялась
            # 2. при нажатии кнопкии отправить callback на разбивку. 3. СЛОВАРИ!!!!!!!!!!!!!!!!!!!!

# buttons
add_time_text = 'Добавить часы'
statistics_time_text = 'Статистика часов'
statistics_time_week_text = 'Статистика за неделю'
statistics_time_month_text = 'Статистика за месяц'
instruction_text = 'Инструкция'
settings_text = 'Настройки'
settings_yes_text = 'Да'
settings_no_text = 'Нет'
no_command_text = 'Я не знаю такой функции'

# return to main menu
return_to_main_menu_text = 'Главное меню'

# buttons into function
statistics_per_week_text = 'Cтатистика за неделю'
statistics_per_month_text = 'Статистика за месяц'
add_how_much_time_text = 'Сколько ты сегодня работал?'
settings_push_text = 'Настройка push уведомлений'
settings_push_question_text = 'Присылать ли Вам напоминание о добавлениии часов?'
push_yes_text = 'Да'
push_no_text = 'Нет'
return_one_step_text = 'Назад'

#text
instruction_into_button_text = 'После команды "start" у Вас появляется главное меню, в котором....'

btn_return_menu = types.KeyboardButton(return_to_main_menu_text)
btn_return_one_step = types.KeyboardButton(return_one_step_text)

@bot.message_handler(commands=['start'])
def start(message):
    # mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    # bot.send_message(message.chat.id, mess, parse_mode='html')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # website = types.KeyboardButton.('')
    text = f"Привет {message.from_user.first_name} {message.from_user.last_name}"
    show_main_menu_func(message, text)


@bot.message_handler(content_types=['text'])
def detected_user_tap(message):
    if message.text == add_time_text:
        add_how_much_time_func(message)

    elif message.text == statistics_time_text:
        statistics_time_func(message)
    elif message.text == instruction_text:
        instruction_func(message)
    elif message.text == settings_text:
        settings_func(message)

    elif message.text == statistics_per_week_text:
        statistics_per_week_func(message)
    elif message.text == statistics_per_month_text:
        statistics_per_month_func(message)
    elif message.text == return_to_main_menu_text:
        return_to_main_menu_func(message)

    elif message.text == add_how_much_time_text:
        add_how_much_time_func(message)

    elif message.text == settings_push_text:
        settings_push_func(message)

    # elif message.text == '8:00':
    #     time_8_func(message)


    else:
        no_command_func(message)




def add_how_much_time_func(message):
    # buttons = [
    #     types.InlineKeyboardButton(text="8:00", callback_data="time_1"),
    #     types.InlineKeyboardButton(text="8:30", callback_data="time_2"),
    #     types.InlineKeyboardButton(text="9:00", callback_data="time_3")
    # ]
    # keyboard = types.InlineKeyboardMarkup(row_width=3)
    # keyboard.add(*buttons)
    # bot.send_message(message.chat.id, text=add_how_much_time_text, reply_markup=buttons)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    time_6_7_btn = types.InlineKeyboardButton(text='6-7', callback_data = 's_hours:6' )
    time_7_8_btn = types.InlineKeyboardButton(text='7-8', callback_data= 's_hours:7')
    time_8_9_btn = types.InlineKeyboardButton(text='8-9', callback_data= 's_hours:8')
    time_9_10_btn = types.InlineKeyboardButton(text='9-10', callback_data= 's_hours:9')
    time_10_11_btn = types.InlineKeyboardButton(text='10-11', callback_data= 's_hours:10')
    time_11_12_btn = types.InlineKeyboardButton(text='11-12', callback_data= 's_hours:11')
    markup_inline.add(time_6_7_btn, time_7_8_btn, time_8_9_btn, time_9_10_btn, time_10_11_btn, time_11_12_btn)
    bot.send_message(message.chat.id, text=add_how_much_time_text, reply_markup=markup_inline)


def add_dict_func(key, value):
    my_dict[key] = value


#callback = s = key:value
def split_callback_func(callback:str):
    s = 'key:value'
    d = s.split(':')
    add_dict_func(d[0], d[1])
    print(my_dict)


# def test_func():
#     s = 'Ivn Idje JIDie'
#     d = s.split()
#     print(d)
#     add_dict_func(d[0], d[1])
#     add_dict_func('1', 'jopa')


# test_func()




def time_quaters_minutes_func(message, hours):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    time_00_btn = types.InlineKeyboardButton(text=hours +':00', callback_data = 's_minutes:00')
    time_15_btn = types.InlineKeyboardButton(text=hours +':15', callback_data = 's_minutes:15')
    time_30_btn = types.InlineKeyboardButton(text=hours +':30', callback_data = 's_minutes:30')
    time_45_btn = types.InlineKeyboardButton(text=hours +':45', callback_data = 's_minutes:45')
    markup_inline.add(time_00_btn, time_15_btn, time_30_btn, time_45_btn)
    bot.send_message(message.chat.id, text='Вы начали работать в ', reply_markup=markup_inline)


# def object_to_json(my_object):
#     res = json.dumps(my_object, cls=MyEncoder)
#     print('json: '+res)



@bot.callback_query_handler(func = lambda call:True)
def answer(callback : types.CallbackQuery):
    time_quaters_minutes_func(callback.message, callback.data)
    split_callback_func(callback.data)
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
    btn_statistics_per_week = types.KeyboardButton(statistics_per_week_text)
    btn_statistics_per_text = types.KeyboardButton(statistics_per_month_text)
    markup.add(statistics_per_week_text, statistics_per_month_text, btn_return_menu)
    bot.send_message(message.chat.id, text=statistics_time_text, reply_markup=markup)


def instruction_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_return_menu)
    bot.send_message(message.chat.id, text=instruction_into_button_text, reply_markup=markup)


def settings_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_settings_push = types.KeyboardButton(settings_push_text)
    markup.add( btn_return_menu)
    bot.send_message(message.chat.id, text=settings_push_text, reply_markup=markup)


def settings_push_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_push_yes = types.KeyboardButton(push_yes_text)
    btn_push_no = types.KeyboardButton(push_no_text)
    markup.add(btn_push_yes, btn_push_no, btn_return_one_step)
    bot.send_message(message.chat.id, text=settings_push_question_text, reply_markup=markup)


def no_command_func(message):
    bot.send_message(message.chat.id, text=no_command_text)


def statistics_per_week_func(message):
    bot.send_message(message.chat.id, text=statistics_time_week_text)


def statistics_per_month_func(message):
    bot.send_message(message.chat.id, text=statistics_time_month_text)


def show_main_menu_func(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add_time = types.KeyboardButton(add_time_text)
    btn_statistics_time = types.KeyboardButton(statistics_time_text)
    btn_instruction = types.KeyboardButton(instruction_text)
    btn_settings = types.KeyboardButton(settings_text)
    markup.add(btn_add_time, btn_statistics_time)
    markup.row(btn_instruction, btn_settings)
    bot.send_message(message.chat.id,
                     text=text.format(message.from_user), reply_markup=markup)


def return_to_main_menu_func(message):
    show_main_menu_func(message, return_to_main_menu_text)

def return_one_step_func(message):
    settings_push_func(message)


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
