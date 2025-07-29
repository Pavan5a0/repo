# repo
this is source code management using git and github lab

## Telegram Movie Search Bot

### Setup

1. Create a Telegram bot via [BotFather](https://t.me/BotFather) and copy the generated token.
2. Clone this repository and install requirements:

```bash
pip install -r requirements.txt
```

3. Export your token in the environment before running:

```bash
export TELEGRAM_TOKEN="<YOUR_TOKEN_HERE>"
```

4. Start the bot:

```bash
python bot.py
```

### Usage

* Send any movie name in a private chat with the bot or in a group where the bot is added.
* The bot will search the following websites:
  * https://www.5movierulz.sarl/
  * https://mp4online1.blogspot.com/
  * https://rts.ibomma.wf/telugu-movies/
  * https://www.watchmovierulz.fi/

If the movie is found on at least one site, the bot replies with the corresponding working search links. Otherwise it responds with `Movie not found`.

The bot also tells you how many times you have used it in the current runtime session.
