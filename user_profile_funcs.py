from wrappers import *
import telebot
from telebot import types
from config import *

'''
* Initialize user profile (only if it is already not initialized)
* when user starts bot (/start).
'''
def user_profile_init(database_file, message):
    data = json_open(database_file)
    if (message.from_user.username not in data):
        data[message.from_user.username] = {"tasks": {}}
    json_write(database_file, data)



'''
* lists user tasks in chat.
* Sends them as inline keyboard.
'''
def list_user_tasks(message):
    data = json_open("db.json")
    tasks = data[message.from_user.username]["tasks"]

    markup = telebot.types.InlineKeyboardMarkup()
    for task_name in tasks:
        callback_dict = json.dumps({"selected task": task_name}) # serealize dict into string to send it as callback data.
        button = telebot.types.InlineKeyboardButton(text=str(task_name) + ". " + tasks[task_name], callback_data=callback_dict)
        markup.add(button)

    if len(tasks) > 0:
    	bot.send_message(message.chat.id, "Okey, there is list of your tasks:", reply_markup=markup)
    else:
    	bot.send_message(message.chat.id, "You don`t have any tasks to do yet.💆‍♂️")



'''
# Moves task with task_id from data[username][from_list] 
# to data[username][to_list].
'''
def move_task_to_another_list(message, task_id, from_list, to_list):
    data = json_open("db.json")
    task = data[message.from_user.username][from_list][task_id]
    data[message.from_user.username][from_list].pop(task_id)
    if to_list not in data[message.from_user.username].keys():
        data[message.from_user.username][to_list] = {}
    new_id = len(data[message.from_user.username][to_list]) + 1
    data[message.from_user.username][to_list][new_id] = task
    json_write("db.json", data)



    
