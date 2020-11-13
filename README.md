# Cheapshot Says
This is an inline telegram bot to generate stickers for cheapshot community with requested text and emoji.

## Telegram usage
`@cheapshot_says_bot`  `emoji` `message.`
Message must end with a dot. 
Spaces between arguments are optional.
You can find a complete list of availiable emojis [here](https://api.cheapshot.co/userpics.html) 

## Python script usage
`python3 makeimage.py` `{emoji}` `"{your message}"` `{output file}` Message must be in quotes. 

Generates .webp file just like bot in Telegram.

## Dependencies
Disclaimer: I do not support this bot on Windows, but it should work fine after some tweaking, so
if you want to port this bot to Windows, feel free to create a pull request.

- `python3` 
- `imagemagick`
- `PyTelegramBotAPI`
- `requests`
- `cwebp`
  - for Arch Linux: `libwebp`
  - `for Debian based distros: `webp`

---
### Bot description
This is an inline telegram bot to generate stickers for cheapshot community with requested text and emoji.

**Usage**
`@cheapshot_says_bot`  `emoji` `message.`
Message must end with a dot. 
Spaces between arguments are optional.
You can find a complete list of availiable emojis [here](https://api.cheapshot.co/userpics.html) .

**Example**
`@cheapshot_says_bot` `👨🏿‍💻` `Kolyahater.`

This bot is developed and maintained by @overaid.
You can submit your feedback with a `/feedback` command in a private chat with this bot.
Issues can be submitted either in the github repository or with a `/issue`  command in a private chat with this bot.
Bot's upstream repository can be found [here](https://github.com/maksmeshkov/cheapshot_says_bot).

Please star this bot on [github](https://github.com/maksmeshkov/cheapshot_says_bot) if you like it!

--- 
## License
This whole project except for all images is distributed under GNU General Public License.
All artworks used in this project are copyright © to Cheapshot Pte. Ltd.
