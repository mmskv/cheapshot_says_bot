#! /usr/bin/python

import os
import subprocess
import time
import sys


class Generator:
    def __init__(self, user_pic, message):
        # TODO add sticker caching to avoid redrawing
        # TODO add passed variables check
        # TODO do not make 2 files for convert
        self.timestamp = int(time.time())
        self.user_pic = user_pic
        self.message = message  # Used by make_text, bubble_builder
        self.output_location = f'assets/generated/{self.timestamp}.png'
        self.webp_location = f'assets/generated_webp/{self.timestamp}.webp'
        self.user_pic_location = f'assets/userpics_png/{self.user_pic}.png'
        self.textPng = False
        self.bubbleWithText = False
        self.line_count = 0
        self.lines = []
        self.formatted_message = ""

    def sticker_generate(self):
        """
        Generating a sticker

        :return:
        Success + sticker location
        """
        self.message_formatter()
        self.make_text()
        self.bubble_builder()
        if self.command_builder():
            self.covert_to_webp()
            return self.webp_location

    def make_text(self):
        """
        Generating a PNG image from given text

        sets text.Png to the
        Location of generated PNG
        """
        for line in self.lines:
            self.formatted_message += line + '\n'
        # Removing trailing newline character
        self.formatted_message = self.formatted_message[:-1]
        os.system(f'convert -font Roboto-Bold  -background none -fill white -gravity center \
                  -pointsize 40 label:"{self.formatted_message}" assets/text/{self.timestamp}_text.png')
        self.textPng = f'assets/text/{self.timestamp}_text.png'

    def bubble_builder(self):
        """
        Resizing blue bubble to fit text png

        sets bubbleWithText to a
        Command to make a bubble with text
        """
        bubble = "assets/bubble.png"
        width = f'identify -format "%w" {self.textPng}'
        # Set bubble height based on line count
        height = 80 if self.line_count == 1 else 120
        # TODO add newline support and change bubble height
        rounder = f'{bubble} -resize $(($({width}) + 60))x{height}! -alpha set -virtual-pixel Transparent \
        -channel A -blur 0x20 -threshold 50% +channel'
        bubble_with_text = rf'\( {rounder} \) {self.textPng} -background none -gravity \
            center -compose over -composite'
        self.bubbleWithText = bubble_with_text

    def command_builder(self):
        """
        Generates a sticker

        .. todo Document this
        """
        if self.bubbleWithText:
            arrow = 'assets/arrow.png'
            if os.path.isfile(self.user_pic_location):
                resize_user_pic = f'{self.user_pic_location} -resize 300x300 -gravity center -extent 512x302'
                command = rf'convert \( {self.bubbleWithText} \) \( {arrow} \) \( {resize_user_pic} \) -append -gravity \
                center -background none -extent 512x512 {self.output_location}'
                os.system(command)
                return True
            else:
                # TODO raise exception to print error message inline
                return False
        else:
            return False, "Text length is too big"

    def covert_to_webp(self):
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['cwebp', self.output_location, '-o', self.webp_location],
                                  stdout=devnull, stderr=subprocess.STDOUT)
        # TODO what is the purpose of this return?
        return True

    def message_formatter(self):
        """
        Sets line_count to amount of lines in final message (2 max)
        Sets lines
        """
        line = ""
        for word in self.message.split(' '):
            if len(self.lines) != 2:
                if len(line) + len(word) <= 17:
                    line += word + ' '
                else:
                    # Removing trailing whitespace
                    self.lines.append(line[:-1])
                    line = word + ' '
            else:
                self.line_count = len(self.lines)
        self.lines.append(line[:-1])
        self.line_count = len(self.lines)


if __name__ == '__main__':
    DEBUG = False

    icon = sys.argv[1]
    msg = sys.argv[2]
    output = sys.argv[3]
    if DEBUG:
        for arg in sys.argv:
            print(arg)

    generator = Generator(icon, msg)
    generator.output_location = output + '.webp'
    print('Icon     \t', icon)
    print('Message  \t', msg)
    generator.sticker_generate()
    print('Generated \t', output+'.webp')
