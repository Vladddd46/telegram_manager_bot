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

from user_profile_funcs import *
from menus import *
from config import *
sessions = {}


'''
# Entry point. User types /start
# 1. Initialize user`s profile if it`s new user.
# 2. Sends welcome text.
# 3. Sends main menu.
'''
@bot.message_handler(commands=['start'])
def initialization(message):
    user_profile_init("db.json", message)
    bot.send_message(message.chat.id, txt_welcome_text)
    main_menu(message)



'''
# Entry point to tasks functional.
# Change main menu view to tasks view.
'''    
@bot.message_handler(regexp=r"^tasks$")
def tasks_view(message):
    list_user_tasks(message)
    tasks_menu(message)

@bot.message_handler(regexp=r"^add new task$")
def add_task(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write new task:", reply_markup=markup)

@bot.message_handler(regexp=r"^remove task$")
def remove_task(message):
    list_user_tasks(message)
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write id of task you want to remove:", reply_markup=markup)


@bot.message_handler(regexp=r"^done ✅$")
def task_done(message):
    data = json_open("db.json")

    try:
        task_id = sessions[message.from_user.username]["selected task"]
        data[message.from_user.username]["tasks"].pop(task_id)
    except:
        pass
    json_write("db.json", data)

    msg = "Good job👍\nNow task is moved to done-tasks list📑"
    list_user_tasks(message)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(regexp=r"^failed ⛔️$")
def task_failed(message):
    data = json_open("db.json")
    print(sessions)
    task_id = sessions[message.from_user.username]["selected task"]
    print(task_id)
    data[message.from_user.username]["tasks"].pop(task_id)
    json_write("db.json", data)
    bot.send_message(message.chat.id, "Update tasks")



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
    callback_data = json.loads(call.data)

    if 'selected task' in callback_data.keys():
        if (call.message.chat.username not in sessions.keys()):
            sessions[call.message.chat.username] = {}
        sessions[call.message.chat.username]["selected task"] = callback_data["selected task"]
        task_close_menu(call)
       
bot.polling()

