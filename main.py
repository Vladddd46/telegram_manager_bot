import telebot
from   telebot import types

from json_api.json_api import *
from config.texts      import *
from config.config     import *

from user_profile_funcs import *
from menus import *
from force_replies import *

database_init("db.json")

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
    if protection(message, "tasks_menu"):
        return;
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write new task:", reply_markup=markup)

@bot.message_handler(regexp=r"^remove task$")
def remove_task(message):
    if protection(message, "tasks_menu"):
        return;
    list_user_tasks(message)
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Write id of task you want to remove:", reply_markup=markup)

@bot.message_handler(regexp=r"^🔙back to main menu$")
def back_to_main_menu(message):
    main_menu(message)

@bot.message_handler(regexp=r"^🔙back to tasks menu$")
def back_to_tasks_menu(message):
    tasks_menu(message)

@bot.message_handler(regexp=r"^🗒show tasks list🗒$")
def show_tasks_list(message):
    if protection(message, "tasks_menu"):
        return;
    list_user_tasks(message)



'''
# Sends list with all done tasks to user.
'''
@bot.message_handler(regexp=r"^done list✅$")
def done_list_show(message):
    if protection(message, "tasks_menu"):
        return;
    list_tasks_from_list(message, "done tasks")
    tasks_menu(message)



'''
# Sends list with all failed tasks to user.
'''
@bot.message_handler(regexp=r"^failed list⛔️$")
def done_list_show(message):
    if protection(message, "tasks_menu"):
        return;
    list_tasks_from_list(message, "failed tasks")
    tasks_menu(message)



'''
# Moves session[username]["selected task"] from data[username]["tasks"] 
# list to data[username]["done list"].
'''
@bot.message_handler(regexp=r"^done ✅$")
def task_done(message):
    if protection(message, "task_selected_menu"):
        return;
    task_id = sessions[message.from_user.username]["selected task"]
    move_task_to_another_list(message, task_id, "tasks", "done tasks")
    msg = "Good job👍\nNow task is moved to done-tasks list📑"
    bot.send_message(message.chat.id, msg)
    list_user_tasks(message)
    tasks_menu(message)



'''
# Moves session[username]["selected task"] from data[username]["tasks"] 
# list to data[username]["failed list"].
'''
@bot.message_handler(regexp=r"^failed ⛔️$")
def task_failed(message):
    if protection(message, "task_selected_menu"):
        return;
    task_id = sessions[message.from_user.username]["selected task"]
    move_task_to_another_list(message, task_id, "tasks", "failed tasks")
    msg = "😢Task is failed😢\nNow task is moved to failed-tasks list📑\n"
    bot.send_message(message.chat.id, msg)
    list_user_tasks(message)
    tasks_menu(message)



@bot.message_handler(content_types=["text"])
def text(message):
    force_replies(message)

    

'''
# Notice: All calback data is sent as serealized in json dict.
# Firstly it`s needed to deserealize callback data and then do some logic.
'''
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    callback_data = json.loads(call.data) # deserealization.

    if 'selected task' in callback_data.keys():
        if (call.message.chat.username not in sessions.keys()):
            sessions[call.message.chat.username] = {}
        sessions[call.message.chat.username]["selected task"] = callback_data["selected task"]
        task_selected_menu(call)

bot.polling()