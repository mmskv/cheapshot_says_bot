#! /usr/bin/python

import os
import subprocess
import time
import sys
import emoji

bots = [':evergreen_tree:', ':deciduous_tree:', ':cactus:', ':rose:',
        ':hibiscus:', ':sunflower:', ':mushroom:', ':dragon:', ':snake:',
        ':pig:', ':octopus:', ':bug:', ':honeybee:', ':lady_beetle:',
        ':front-facing_baby_chick:', ':dolphin:', ':alien_monster:',
        ':skull:', ':fire:', ':squid:', ':hedgehog:', ':T-Rex:', ':parrot:']


class Generator:
    def __init__(self, user_pic, message):
        # TODO add sticker caching to avoid redrawing
        # TODO add passed variables check
        # TODO do not make 2 files for convert
        self.timestamp = int(time.time())
        self.user_pic = emoji.demojize(user_pic)
        self.message = message[0].upper() + message[1:]
        self.output_location = f'assets/generated/{self.timestamp}.png'
        self.webp_location = f'assets/generated_webp/{self.timestamp}.webp'
        self.user_pic_location = f'assets/userpics_png/{self.user_pic}.png'
        self.is_bot = False
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
        if self.user_pic in bots:
            self.is_bot = True
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
        os.system(rf'convert -background none -fill white -gravity center \
                  pango:"<span font_desc=\'SF Pro Display Heavy\' size=\'30000\'>{self.formatted_message}</span>" \
                  assets/text/{self.timestamp}_text.png')
        self.textPng = f'assets/text/{self.timestamp}_text.png'

    def bubble_builder(self):
        """
        Resizing blue bubble to fit text png

        sets bubbleWithText to a
        Command to make a bubble with text
        """
        bubble = "assets/bubble-grey.png" if self.is_bot else "assets/bubble.png"
        width = f'identify -format "%w" {self.textPng}'
        # Set bubble height based on line count
        if self.line_count == 1:
            height = 80
            width_offset = 60
        elif self.line_count == 2:
            height = 120
            width_offset = 70
        else:
            height = 160
            width_offset = 80
        radius = height // 2
        # TODO add newline support and change bubble height
        rounder = rf"{bubble} -resize $(($({width}) + {width_offset}))x{height}! \( +clone  -alpha extract \
         -draw 'fill black polygon 0,0 0,{radius} {radius},0 fill white circle {radius},{radius} {radius},0' \
              \( +clone -flip \) -compose Multiply -composite \
              \( +clone -flop \) -compose Multiply -composite \
           \) -alpha off -compose CopyOpacity -composite"

        bubble_with_text = rf'\( {rounder} \) {self.textPng} -background none -gravity \
            center -compose over -composite'
        self.bubbleWithText = bubble_with_text

    def command_builder(self):
        """
        Generates a sticker

        .. todo Document this
        """
        if self.bubbleWithText:
            arrow = "assets/arrow-grey.png" if self.is_bot else "assets/arrow.png"
            if os.path.isfile(self.user_pic_location):
                resize_user_pic = f'{self.user_pic_location} -resize 280x280 -gravity center -extent 512x280'
                command = rf'convert \( {self.bubbleWithText} \) \( {arrow} \) \( {resize_user_pic} \) -append -gravity \
                center -background none -extent 512x512 {self.output_location}'
                os.system(command)
                return True
            else:
                # TODO raise exception to print error message inline
                return False
        else:
            return False

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
        # TODO Remake this shit code
        _message = self.message.split(' ')
        for word in self.message.split(' '):
            if len(line) + len(word) <= 19:
                line += word + ' '
            else:
                if self.line_count < 3:
                    self.lines.append(line[:-1])
                    self.line_count += 1
                    line = word + ' '
                else:
                    return
        if self.line_count < 3 and line != " ":
            self.lines.append(line[:-1])
            self.line_count += 1


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
    print('Generated \t', output + '.webp')
