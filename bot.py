#! /usr/bin/python
import re
from datetime import time

import telebot
from telebot import types
import makeimage
from random import random
import sys

token_file = open('.token', 'r')
tg_token = token_file.read()
log_chat_id = -429428708

if tg_token is None:
    print("API token empty")
    exit()
else:
    print(f"Token {tg_token} loaded")

# Using Async may bring some trouble
bot = telebot.TeleBot(tg_token)


@bot.inline_handler(lambda query: re.match(r'.+ [\'\"”„“«»].+[\'\"”„“«»]', query.query) is not None)
def query_request(inline_query):
    try:
        print(inline_query)
        try:
            print(f"Query \'{inline_query.query}\'")
            user_pic = re.search(r'\s*([^\s]+)\s*[\',\",\”,\„,\“,\«,\»].+[\',\",\”,\„,\“,\«,\»]', inline_query.query).group(1)
            print(f"user_pic = {user_pic}")
            message = re.search('.+[\'\"”„“«»](.+)[\'\"”„“«»]', inline_query.query).group(1)
        except AttributeError:
            user_pic = '🐷'
            message = 'emoji not found'
        generator = makeimage.Generator(user_pic, message)
        sticker_location = generator.sticker_generate()
        print(f"Generated sticker {user_pic} {message}")
        file = open(sticker_location, 'rb')
        print(f"Opened sticker {user_pic} {message}")
        bot.send_message(log_chat_id, inline_query.from_user.first_name + " @" + inline_query.from_user.username)
        file_id = bot.send_document(log_chat_id, file).sticker.file_id
        r = types.InlineQueryResultCachedSticker(id=int(random()*10000000000000000),
                                                 sticker_file_id=file_id, )
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['ping'])
# Query must end with comma
# TODO add async if it is faster
def send_welcome(message):
    bot.reply_to(message, "/pong")


@bot.message_handler(commands=['pong'])
def send_welcome(message):
    bot.reply_to(message, "/ping")


def main():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
