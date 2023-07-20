## Installation

To run the code in this repository, you need to install the following dependencies:

- `bardapi`: Use the following command to install the `bardapi` library:
  ```
  pip install bardapi
  ```

- `python-telegram-bot`: Use the following command to install the `python-telegram-bot` library version 12.8:
  ```
  pip install python-telegram-bot==12.8
  ```


## Authentication
### Bard API
> **Warning** Do not expose the `__Secure-1PSID` 
1. Visit https://bard.google.com/
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie.

Note that while I referred to `__Secure-1PSID` value as an API key for convenience, it is not an officially provided API key. 
Cookie value subject to frequent changes. Verify the value again if an error occurs. Most errors occur when an invalid cookie value is entered.

<br>

If you need to set multiple Cookie values

- [Bard Cookies](https://github.com/dsdanielpark/Bard-API/blob/main/README_DEV.md#bard-which-can-get-cookies) - After confirming that multiple cookie values are required to receive responses reliably in certain countries, I will deploy it for testing purposes. Please debug and create a pull request

<br>

### Telegram Bot
 
1. Create a new bot on Telegram by contacting [@BotFather](https://t.me/BotFather)
2. Follow the instructions to create a new bot and obtain a telegram bot token.