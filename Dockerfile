FROM python:3.10.1-buster

RUN apt-get update

WORKDIR /usr/src/cheapshot-says

COPY requirements.txt .

RUN pip install -qq --no-cache-dir -r requirements.txt

RUN wget https://github.com/sahibjotsaggu/San-Francisco-Pro-Fonts/raw/master/SF-Pro-Display-Heavy.otf
RUN mkdir /usr/local/share/fonts/opentype
RUN mv SF-Pro-Display-Heavy.otf /usr/local/share/fonts/opentype/

RUN wget https://github.com/samuelngs/apple-emoji-linux/releases/download/ios-15.4/AppleColorEmoji.ttf
RUN mv AppleColorEmoji.ttf /usr/local/share/fonts
RUN fc-cache

RUN apt-get install -y imagemagick webp

COPY . .

RUN mkdir assets/text

CMD python3 bot.py
