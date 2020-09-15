import telebot
from telebot import types
import json

'''
 * This is manager bot for telegram project.
 * ...
'''

bot = telebot.TeleBot("1312682990:AAERtIGXkjIMbgyKx__6Tu-fZqabVk9imCs")

@bot.message_handler(commands=['start'])
def initialization(message):
    msg = "Hello!\nMy name is Karl and I am the manager bot.\n I want to be your assistant.\n\
    I can help you structure all your task and notify you about deadlines.\n\
    I can remind you about birthdays.\n\
    I can track you budget.\n And many many other thing...\n\
    Write /help for more details."

    with open("db.json", "r") as f:
        data = json.load(f)
    if (message.from_user.username not in data):
        data[message.from_user.username] = {"tasks": ["t1", "t2", "t3"]}
    with open("db.json", "w") as f:
        json.dump(data, f, indent=2)

    markup     = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('tasks')
    itembtna   = types.KeyboardButton('a')
    itembtnb   = types.KeyboardButton('b')
    itembtnc   = types.KeyboardButton('c')

    markup.row(item_tasks, itembtna)
    markup.row(itembtnb, itembtnc)
    bot.send_message(message.chat.id, msg, reply_markup=markup)



@bot.message_handler(content_types=['text'])
def tasks_menu(message):
    with open("db.json", "r") as f:
        data = json.load(f)

    tasks = data[message.from_user.username]["tasks"]
    markup = telebot.types.InlineKeyboardMarkup()
    for i in tasks:
        button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
        markup.add(button)


    bot.send_message(message.chat.id, "You tasks:", reply_markup=markup)

bot.polling()


# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     if call.data == 'add':
#         bot.answer_callback_query(callback_query_id=call.id, text='Hello world')
