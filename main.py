import telebot
from telebot import types
import json
from wrappers import *


'''
# texts module contains variables with texts sended by bot.
# This is done to simplify editing of texts.
# All variables from this module start with `txt_` prefix
'''
from texts import *


bot = telebot.TeleBot("1312682990:AAERtIGXkjIMbgyKx__6Tu-fZqabVk9imCs")
sessions = {}

'''
* Initialize user profile (only if it is already not initialized)
* when user starts bot (/start).
'''
def user_profile_init(database_file, message):
    data = json_open(database_file)
    if (message.from_user.username not in data):
        data[message.from_user.username] = {"tasks": {}}
    json_write(database_file, data)


def main_menu(message):
    markup     = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('tasks')
    markup.row(item_tasks)

    msg = "Choose the option below:"
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def task_close_menu(call):
    markup           = types.ReplyKeyboardMarkup()
    item_task_done   = types.KeyboardButton('done ✅')
    item_task_failed = types.KeyboardButton('failed ⛔️')

    markup.row(item_task_done, item_task_failed)
    msg = "Task is: "
    bot.send_message(call.message.chat.id, msg, reply_markup=markup)



@bot.message_handler(commands=['start'])
def initialization(message):
    user_profile_init("db.json", message)
    bot.send_message(message.chat.id, txt_welcome_text)
    main_menu(message)



'''
* lists user tasks in chat.
* Sends them as inline keyboard.
'''
def list_user_tasks(message):
    data = json_open("db.json")
    tasks = data[message.from_user.username]["tasks"]
    markup = telebot.types.InlineKeyboardMarkup()
    for i in tasks:
        button = telebot.types.InlineKeyboardButton(text=str(i) + ". " + tasks[i], callback_data="task: " + str(i))
        markup.add(button)
    bot.send_message(message.chat.id, "Okey, there is list of your tasks:", reply_markup=markup)


@bot.message_handler(regexp="tasks")
def tasks_menu(message):
    list_user_tasks(message)

    markup1               = types.ReplyKeyboardMarkup(row_width=2)
    add_task_btn          = types.KeyboardButton('add new task')
    ramove_task_btn       = types.KeyboardButton('remove task')
    back_to_main_menu_btn = types.KeyboardButton('back to main menu')
    markup1.row(add_task_btn, ramove_task_btn)
    markup1.row(back_to_main_menu_btn)
    bot.send_message(message.chat.id, "Click on task to edit it\nTo add/remove new task choose the option below.\n⬇️⬇️⬇️⬇️⬇️", reply_markup=markup1)



@bot.message_handler(regexp="add new task")
def add_new_task(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write new task:", reply_markup=markup)





@bot.message_handler(content_types=["text"])
def replies(message):
    data = json_open("db.json")
    try:
        if message.reply_to_message.text == "Write new task:":
            task_id = len(data[message.from_user.username]["tasks"]) + 1
            data[message.from_user.username]["tasks"][task_id]  = message.text
        json_write("db.json", data)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    if call.data[0:6] == 'task: ':
        task_close_menu(call)
       
bot.polling()

