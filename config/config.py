import telebot
from telebot import types

bot = telebot.TeleBot("1312682990:AAERtIGXkjIMbgyKx__6Tu-fZqabVk9imCs")


'''
# Stores data about user`s current state.
# session[user_name]["selected task"] - task user has selected in inline keyboard.
# session[user_name]["current menu"]  - menu, which is opened.
'''
sessions = {}