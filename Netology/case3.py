# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk
"""

import telebot

TOKEN = '391071743:AAEVwwb52k-XUrxFiTNicxy5yfimSiuJiNA'

bot = telebot.TeleBot(TOKEN)

OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}


@bot.message_handler(content_types=["text"])
def calculate(message): # Название функции не играет никакой роли, в принципе
    code = (message.text)
    bot.send_message(message.chat.id, code)


if __name__ == '__main__':
    bot.polling(none_stop=True)