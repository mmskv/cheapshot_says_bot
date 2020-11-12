#! /usr/bin/python

import os
from time import time_ns
import sys


def log(string):
    if DEBUG:
        print(string)


class Generator:
    def __init__(self, user_pic, message):
        # TODO add passed variables check
        self.timestamp = time_ns()
        self.user_pic = user_pic
        self.message = message  # Used by make_text, bubble_builder
        self.output_location = f'assets/generated/{self.timestamp}.png'
        self.user_pic_location = f'assets/userpics_png/{self.user_pic}.png'
        self.textPng = False
        self.bubbleWithText = False

    def sticker_generate(self):
        """
        Generating a sticker

        :return:
        Success + sticker location
        """
        self.make_text()
        self.bubble_builder()
        self.command_builder()
        print(f'Sticker generated \nText = {self.message}\nIcon = {self.user_pic}')
        return True, self.output_location

    def make_text(self):
        """
        Generating a PNG image from given text

        sets text.Png to the
        Location of generated PNG
        """
        if DEBUG:
            print(self.timestamp, "  '", self.message, "'")
        os.system(f'convert -font Roboto-Bold  -background none -fill white -gravity center \
                  -pointsize 40 label:"{self.message}" assets/text/{self.timestamp}_text.png')
        self.textPng = f'assets/text/{self.timestamp}_text.png'

    def bubble_builder(self):
        """
        Resizing blue bubble to fit text png

        sets bubbleWithText to a
        Command to make a bubble with text
        """
        width = f'identify -format "%w" {self.textPng}'
        bubble = "assets/bubble.png"
        # TODO add newline support and change bubble height
        rounder = f'{bubble} -resize $(($({width}) + 60))x80! -alpha set -virtual-pixel Transparent \
        -channel A -blur 0x20 -threshold 50% +channel'
        bubble_with_text = rf'\( {rounder} \) {self.textPng} -background none -gravity \
            center -compose over -composite'
        log('bubble with text: ' + bubble_with_text)
        self.bubbleWithText = bubble_with_text

    def command_builder(self):
        """
        Generates a sticker

        .. todo Document this
        """
        if self.bubbleWithText:
            arrow = 'assets/arrow.png'
            # TODO check if user_pic_location exists
            resize_user_pic = f'{self.user_pic_location} -resize 300x300 -gravity center -extent 512x302'
            command = rf'convert \( {self.bubbleWithText} \) \( {arrow} \) \( {resize_user_pic} \) -append -gravity \
            center -background none -extent 512x512 {self.output_location}'
            os.system(command)
            return True
        else:
            return False, "Text length is too big"


if __name__ == '__main__':
    DEBUG = False

    icon = sys.argv[1]
    msg = sys.argv[2]
    output = sys.argv[3]
    if DEBUG:
        for arg in sys.argv:
            print(arg)

    generator = Generator(icon, msg)
    generator.output_location = output
    generator.sticker_generate()
