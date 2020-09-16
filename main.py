import telebot
from telebot import types
import json

'''
 * This is manager bot for telegram project.
 * ...
'''

def json_open(file_name):
    data = None
    with open(file_name, "r") as f:
        data = json.load(f)

    if type(data) != dict:
        print("Some error occured, while opening json file.")
    return data

def json_write(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)



bot = telebot.TeleBot("1312682990:AAERtIGXkjIMbgyKx__6Tu-fZqabVk9imCs")

@bot.message_handler(commands=['start'])
def initialization(message):
    msg = "Hello!\nMy name is Karl and I am the manager bot.\n I want to be your assistant.\n\
    I can help you structure all your task and notify you about deadlines.\n\
    I can remind you about birthdays.\n\
    I can track you budget.\n And many many other thing...\n\
    Write /help for more details."

    data = json_open("db.json")
    if (message.from_user.username not in data):
        data[message.from_user.username] = {"tasks": {}}
    json_write("db.json", data)

    markup     = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('tasks')
    itembtna   = types.KeyboardButton('a')
    itembtnb   = types.KeyboardButton('b')
    itembtnc   = types.KeyboardButton('c')

    markup.row(item_tasks, itembtna)
    markup.row(itembtnb, itembtnc)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.message_handler(regexp="tasks")
def tasks_menu(message):
    data = json_open("db.json")

    tasks = data[message.from_user.username]["tasks"]
    markup = telebot.types.InlineKeyboardMarkup()
    for i in tasks:
        button = telebot.types.InlineKeyboardButton(text=tasks[i], callback_data=i)
        markup.add(button)


    bot.send_message(message.chat.id, "Tasks need to be completed:", reply_markup=markup)

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
bot.polling()


# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     if call.data == 'add':
#         bot.answer_callback_query(callback_query_id=call.id, text='Hello world')
