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
    for i in tasks:
        callback_dict = json.dumps({"selected task": i}) # serealize dict into string to send it as callback data.
        button = telebot.types.InlineKeyboardButton(text=str(i) + ". " + tasks[i], callback_data=callback_dict)
        markup.add(button)

    if len(tasks) > 0:
    	bot.send_message(message.chat.id, "Okey, there is list of your tasks:", reply_markup=markup)
    else:
    	bot.send_message(message.chat.id, "You don`t have any tasks to do yet.💆‍♂️")