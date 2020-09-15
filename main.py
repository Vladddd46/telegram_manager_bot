import telebot
from telebot import types

'''
 * This is manager bot for telegram project.
 * ...
'''

bot = telebot.TeleBot("token")


@bot.message_handler(commands=['start'])
def initialization(message):
    msg = "Hello!\nMy name is Karl and I am the manager bot.\n I want to be your assistant.\n\
    I can help you structure all your task and notify you about deadlines.\n\
    I can remind you about birthdays.\n\
    I can track you budget.\n And many many other thing...\n\
    Write /help for more details."

    markup = types.ReplyKeyboardMarkup()
    item_tasks = types.KeyboardButton('/tasks')
    itembtna = types.KeyboardButton('a')
    itembtnb = types.KeyboardButton('b')
    itembtnc = types.KeyboardButton('c')
    itembtnd = types.KeyboardButton('d')

    markup.row(item_tasks, itembtna)
    markup.row(itembtnb, itembtnc, itembtnd)

    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.message_handler(commands=['tasks'])
def tasks_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_tasks_show   = types.KeyboardButton('/show_tasks')
    item_tasks_add    = types.KeyboardButton('/add_task')
    item_tasks_edit   = types.KeyboardButton('/edit_task')
    item_tasks_remove = types.KeyboardButton('/remove_task')
    markup.add(item_tasks_show, item_tasks_add, item_tasks_edit, item_tasks_remove)
    bot.send_message(message.chat.id, "d", reply_markup=markup)

bot.polling()

# markup = telebot.types.InlineKeyboardMarkup()
# button = telebot.types.InlineKeyboardButton(text='CLick me', callback_data='add')
# markup.add(button)
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     if call.data == 'add':
#         bot.answer_callback_query(callback_query_id=call.id, text='Hello world')
