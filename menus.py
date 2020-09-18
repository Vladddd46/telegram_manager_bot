import telebot
from telebot import types
from config import *

'''
# Sends main menu keyboard.
'''
def main_menu(message):
    markup     = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('tasks')
    markup.row(item_tasks)

    msg = "Choose the option below:"
    bot.send_message(message.chat.id, msg, reply_markup=markup)

'''
# Menu, which is showed when user clicks on task in inline keyboard. 
'''
def task_close_menu(call):
    markup           = types.ReplyKeyboardMarkup()
    item_task_done   = types.KeyboardButton('done ✅')
    item_task_failed = types.KeyboardButton('failed ⛔️')

    markup.row(item_task_done, item_task_failed)
    msg = "Task is: "
    bot.send_message(call.message.chat.id, msg, reply_markup=markup)