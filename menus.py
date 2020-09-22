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
# Menu, which is showed when user typed `tasks`
'''
def tasks_menu(message):
    markup                = types.ReplyKeyboardMarkup(row_width=2)
    add_task_btn          = types.KeyboardButton('add new task')
    remove_task_btn       = types.KeyboardButton('remove task')
    show_tasks_btn        = types.KeyboardButton('🗒show tasks list🗒')
    back_to_main_menu_btn = types.KeyboardButton('🔙back to main menu')
    done_list_btn         = types.KeyboardButton('done list✅')
    failed_list_btn       = types.KeyboardButton('failed list⛔️')

    markup.row(add_task_btn, remove_task_btn)
    markup.row(show_tasks_btn)
    markup.row(done_list_btn, failed_list_btn)
    markup.row(back_to_main_menu_btn)
    bot.send_message(message.chat.id, "Choose the option below:", reply_markup=markup)

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

