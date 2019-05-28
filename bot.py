import telebot
import datetime
from telebot import types
import misc
import os


bot = telebot.TeleBot(misc.token)
global path

@bot.message_handler(content_types=['text'])
def message(message):
    global path
    keyboard = types.ReplyKeyboardRemove()
    print('[{}] {}: {}'.format(datetime.datetime.now(), message.from_user.username, message.text))

    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет', reply_markup=keyboard)

    if message.text.split()[0] == '/dir':
        files = []

        if len(message.text.split()) > 2:
            keyboard_width = message.text.split()[2]
        else:
            keyboard_width = str(misc.keyboard_width)

        if len(message.text.split()) == 1:
            bot.send_message(message.chat.id, '/dir [path] [keyboard_width=misc.keyboard_width]', reply_markup=keyboard)
        else:
            path = message.text.split()[1]
            files_buffer = os.listdir(path)
            for file in files_buffer:
                if len(file.split('.')) == 2: files.append(file)
            keyboard = types.InlineKeyboardMarkup()

            if keyboard_width == '1':
                for file in files: keyboard.add(types.InlineKeyboardButton(text=file, callback_data=file))
            if keyboard_width == '2':
                for file in range(1, len(files) // 2 * 2, 2):
                    button1 = types.InlineKeyboardButton(text=files[file - 1], callback_data=path + '/' + files[file - 1])
                    button2 = types.InlineKeyboardButton(text=files[file], callback_data=path + '/' + files[file])
                    keyboard.add(button1, button2)
                if len(files) / 2 - len(files) // 2 != 0:
                    keyboard.add(types.InlineKeyboardButton(text=files[-1], callback_data=path + '/' + files[-1]))

            bot.send_message(message.chat.id, 'Директория: {}\nНайдено файлов: {}'.format(path, len(files)), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def call_back_room(call):
    print('Start {}... '.format(call.data), end='')
    os.system(call.data)

bot.polling()
