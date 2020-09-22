import telebot
from telebot import types
from json_api.json_api import *



bot = telebot.TeleBot("1312682990:AAERtIGXkjIMbgyKx__6Tu-fZqabVk9imCs")


'''
# Stores data about user`s current state.
# session[user_name]["selected task"] - task user has selected in inline keyboard.
# session[user_name]["current menu"]  - menu, which is opened.
'''
sessions = {}



'''
# Creates database file, if it does not exist.
'''
def database_init(name):
    try:
        data = json_open(name)
    except:
        data = {}
        json_write(name, data)


