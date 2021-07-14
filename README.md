# Cheapshot Says

This is an inline telegram bot to generate stickers for Cheapshot community
with requested text and emoji.

The goal of this bot is to get as close to the Cheapshot's message rendering as
possible.

## Telegram usage

`@cheapshot_says_bot` `emoji` `message.`
Message must end with a dot.
Spaces between arguments are optional.
You can find a complete list of availiable emojis
[here](https://api.cheapshot.co/userpics.html)

## Python script usage

`python3 makeimage.py` `{emoji}` `"{your message}"` `{output file}` Message
must be in quotes.

Generates .webp file just like the bot in Telegram (useful for stickerpack
creation).

## Deploy with Docker

```sh
git clone https://github.com/mmskv/cheapshot_says_bot
cd cheapshot_says_bot
vim .token # Paste your telegram token here and save
docker build -t cheapshot_says_bot:1.0 .
docker run -d --restart unless-stopped --name cheapshot cheapshot_says_bot:1.0
```

### Dependencies

- `python3`
- `imagemagick`
- `cwebp`
  - for Arch Linux: `libwebp`
  - for Debian based distros: `webp`
- `SF Pro Display Heavy` can be downloaded [here](https://github.com/sahibjotsaggu/San-Francisco-Pro-Fonts)

---

### Bot description

This is an inline telegram bot to generate stickers for Cheapshot community
with requested text and emoji.

The goal of this bot is to get as close to the Cheapshot's message rendering as possible.

**Usage**
`@cheapshot_says_bot`  `emoji` `message.`
Message must end with a dot.
Spaces between arguments are optional.
You can find a complete list of availiable emojis
[here](https://api.cheapshot.co/userpics.html).

**Example**
`@cheapshot_says_bot` `👨🏿‍💻` `Kolyahater.`

This bot is developed and maintained by @overaid.
Issues and feedback can be submitted in the github repository.
Bot's upstream repository can be found [here](https://github.com/maksmeshkov/cheapshot_says_bot).

Please star this bot on
[github](https://github.com/maksmeshkov/cheapshot_says_bot) if you like it!

---

## License

This project except for images in `assets/` is distributed under GNU General
Public License. All artworks used in this project are copyright © to Cheapshot
Pte. Ltd.
