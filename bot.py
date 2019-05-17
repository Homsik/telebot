import os
import telebot
from telebot import types
import misc
import re

bot = telebot.TeleBot(misc.token)
reg = re.compile('[\W\D+]')

@bot.messge_handler(commands=['/start'])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in os.listdir()])
    msg = bot.send_message(m.chat.id, 'Привет.', reply_markup=keyboard)
    bot.register_next_step_handler(msg, name)

def name(m):
    pass

bot.polling()
