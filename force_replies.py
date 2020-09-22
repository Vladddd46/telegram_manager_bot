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
    task_id = len(data[message.from_user.username]["tasks"]) + 1
    data[message.from_user.username]["tasks"][task_id]  = message.text
    json_write("db.json", data)
    list_user_tasks(message)
    tasks_menu(message)



# removes task from data[username]["tasks"]
def rm_task(message):
    data = json_open("db.json")
    task_id = message.text
    if "tasks" not in data[message.from_user.username].keys():
        data[message.from_user.username]["tasks"] = {}
    if task_id in data[message.from_user.username]["tasks"].keys():
        data[message.from_user.username]["tasks"].pop(task_id)
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






