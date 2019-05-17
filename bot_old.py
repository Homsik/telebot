# -*- coding: utf-8 -*-
import requests
import re
import functions
import misc


def getUpdates(): #Данные по боту, получение обновлений
    url = URL + "getUpdates"
    r = requests.get(url)
    return r.json()

def getMessage(): #Получение сообщеня
    data = getUpdates()
    chat_id = data["result"][-1]["message"]["chat"]["id"]
    message_text = data["result"][-1]["message"]["text"]

    message = {"chat_id": chat_id, "text": message_text}
    return message

def sendMessage(chat_id, text='Wait...'): #Отправление сообщения
    url = URL + f"sendMessage?chat_id={chat_id}&text={text}"
    requests.get(url)

def main(): #Планируется вебхук
    update = 0
    while True:
        if getUpdates()["result"] != []:
            if getUpdates()["result"][-1]["update_id"] != update:
                answer = getMessage()
                chat_id = answer['chat_id']
                text = answer['text']

                #Можно перенести в отдельный файл: проверка сообщения и ответ
                if 'привет' in (recompile.sub('', text)).lower(): #Здаровается
                    sendMessage(chat_id, "Привет.")

                if "какаятемпературавперми" in (recompile.sub('', text)).lower(): #Запрос на температуру
                    sendMessage(chat_id, "Температура в Перми равна {}.".format(functions.parse()))
                update = getUpdates()["result"][-1]["update_id"]


token = misc.token #Токен для бота
URL = f'https://api.telegram.org/bot{token}/'
recompile = re.compile("[\W]")
if __name__ == "__main__":
    main()
