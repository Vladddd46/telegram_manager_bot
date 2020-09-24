from json_api.json_api import *
from config.texts      import *
from config.config     import *
from user_profile_funcs import *
from menus import *
import telebot
from telebot import types

'''
# Logic of handling force replies from user.
'''



# adds task to data[username]["tasks"]
def new_task(message):
    data    = json_open("db.json")
    user    = str(message.chat.id)
    task_id = len(data[user]["tasks"]) + 1
    data[user]["tasks"][task_id]  = message.text
    json_write("db.json", data)
    list_user_tasks(message)
    tasks_menu(message)



# removes task from data[username]["tasks"]
def rm_task(message):
    data    = json_open("db.json")
    task_id = message.text
    user    = str(message.chat.id)
    if "tasks" not in data[user].keys():
        data[user]["tasks"] = {}
    if task_id in data[user]["tasks"].keys():
        data[user]["tasks"].pop(task_id)
        msg = "🔻Task is successfully removed🔻"
    else:
        msg = "🔻There is no task with such id🔻"
    json_write("db.json", data)
    id_update(message, "tasks")
    bot.send_message(message.chat.id, msg)
    list_user_tasks(message)
    tasks_menu(message)



def force_replies(message):
    if message.reply_to_message != None and message.reply_to_message.text == "Write new task:":
        new_task(message)
    elif message.reply_to_message != None and message.reply_to_message.text == "Write id of task you want to remove:":
        rm_task(message)






