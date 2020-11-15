#! /usr/bin/python
import logging
import re
import time
import telebot
from telebot import types
import makeimage
from random import random
import sys

token_file = open('.token', 'r')
tg_token = token_file.read().split('\n')[0]
help_message = open('assets/helpmessage.txt', 'r').read()
DEBUG = True
# TODO move token and log_chat_id to .env file
log_chat_id = -429428708

if tg_token is None:
    print("API token empty")
    exit()
else:
    print(f"Token {tg_token} loaded")


def log(string):
    if DEBUG:
        print(string)


# Using Async may bring some trouble
bot = telebot.TeleBot(tg_token)
telebot.logger.setLevel(logging.DEBUG)


@bot.inline_handler(lambda query: re.match(r'.+\.', query.query) is not None)
# TODO add async if it is faster
def query_request(inline_query):
    try:
        try:
            # Parse emoji and message
            user_pic = re.search(r'\s*([^\w\s]{1,4})\s*.+', inline_query.query).group(1)
            message = re.search(r'\s*[^\w\s]{1,4}\s*(.+)\.', inline_query.query).group(1)
            # Open generated sticker
            file = open(makeimage.Generator(user_pic, message).sticker_generate(), 'rb')
            # Send username that requested sticker to logging chat
            if inline_query.from_user.username:
                bot.send_message(log_chat_id, inline_query.from_user.first_name + " @" + inline_query.from_user.username
                                 + '\n' + message)
            else:
                bot.send_message(log_chat_id, inline_query.from_user.first_name + '\n' + message)
            # Send generated sticker to logging chat
            file_id = bot.send_document(log_chat_id, file).sticker.file_id
            # Log query for easier debug
            if inline_query.from_user.username:
                log('Generated sticker for @' + inline_query.from_user.username + ' with query ' + inline_query.query)
            else:
                log('Generated sticker for @' + inline_query.from_user.first_name + ' with query ' + inline_query.query)
            # Offer sticker in inline mode
            sticker = types.InlineQueryResultCachedSticker(id=int(random() * (10 ** 10)), sticker_file_id=file_id)
            bot.answer_inline_query(inline_query.id, [sticker])
        except AttributeError:
            # TODO make this a text instead of a button
            # r = types.InlineQueryResultArticle(id=int(random()*10000000000000000),
            #                                    text="Sticker not found. You can see syntax at bot\'s github repository.")
            # bot.answer_inline_query(inline_query.id, [r])
            pass
    except Exception as e:
        print(e)


@bot.message_handler(commands=['ping'])
def send_welcome(message):
    bot.reply_to(message, "/pong")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, help_message, parse_mode='Markdown')


def main():
    bot.polling(True)
    while True:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
