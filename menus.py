import telebot
from telebot import types
from config.config import *



'''
# Determines user`s current menu and protecs from inappropriate logic.
# If command is called from not appropriate menu(menu_name), returns 1,
# otherwise returns 0.
'''
def protection(message, menu_name):
    user = str(message.chat.id)
    if user not in sessions.keys():
        sessions[user] = {}
    if sessions[user]["current menu"] != menu_name:
        return 1
    return 0



'''
# Sends main menu keyboard.
'''
def main_menu(message):
    markup     = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('tasks')
    markup.row(item_tasks)

    msg = "Choose the option below:"
    bot.send_message(message.chat.id, msg, reply_markup=markup)

    user = str(message.chat.id)
    if user not in sessions.keys():
        sessions[user] = {}
    sessions[user]["current menu"] = "main_menu"

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
    user = str(message.chat.id)
    if user not in sessions.keys():
        sessions[user] = {}
    sessions[user]["current menu"] = "tasks_menu"

'''
# Menu, which is showed when user clicks on task in inline keyboard. 
'''
def task_selected_menu(call):
    markup             = types.ReplyKeyboardMarkup()
    item_task_done     = types.KeyboardButton('done ✅')
    item_task_failed   = types.KeyboardButton('failed ⛔️')
    back_to_tasks_menu = types.KeyboardButton('🔙back to tasks menu')

    markup.row(item_task_done, item_task_failed)
    markup.row(back_to_tasks_menu)
    msg = "Task is: "
    bot.send_message(call.message.chat.id, msg, reply_markup=markup)
    user = str(call.message.chat.id)
    if user not in sessions.keys():
        sessions[user] = {}
    sessions[user]["current menu"] = "task_selected_menu"

