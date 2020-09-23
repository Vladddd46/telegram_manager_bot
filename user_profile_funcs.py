from json_api.json_api import *
import telebot
from telebot import types
from config.config import *

'''
# Contains functions for manipulating
# with user`s profile.
'''


'''
* Initialize user profile (only if it is already not initialized)
* when user starts bot (/start).
'''
def user_profile_init(database_file, message):
    data = json_open(database_file)
    print(message)
    if message.from_user.username not in data.keys():
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
    	bot.send_message(message.chat.id, "📌Okey, there is list of your tasks.📌\n⚙️Click on task to edit it⚙️", reply_markup=markup)
    else:
    	bot.send_message(message.chat.id, "You don`t have any tasks to do yet.💆‍♂️")



'''
# Sends user tasks from list_name.
'''
def list_tasks_from_list(message, list_name):
    data = json_open("db.json")
    if list_name in data[message.from_user.username].keys() and len(data[message.from_user.username][list_name]) != 0:
        tasks = data[message.from_user.username][list_name]
        msg = list_name.capitalize() + ":\n"
        for i in tasks:
            msg += i + ". " + tasks[i] + "\n"
    else:
        msg = "💁" + list_name.capitalize() + " list is empty" +"💁‍♂️"
    bot.send_message(message.chat.id, msg)



'''
# Updates ids in data[username][list_name].
# It`s needed, if some tasks were removed from list_name
'''
def id_update(message, list_name):
    data = json_open("db.json")
    dict_to_update = data[message.from_user.username][list_name]
    new_dict = {}
    for i in dict_to_update:
        new_id           = len(new_dict) + 1
        new_dict[new_id] = dict_to_update[i]
    data[message.from_user.username][list_name] = new_dict
    json_write("db.json", data)



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
    id_update(message, from_list)



    
