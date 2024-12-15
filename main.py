from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageIdInvalid, ChatAdminRequired, EmoticonInvalid, ReactionInvalid
from random import choice
from bot import TelegramBot, logger
from bot.config import Telegram
from logging import getLogger
from os import environ as env

LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'bot': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'pyrogram': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}

@TelegramBot.on_message(filters.all)
async def send_reaction(_, msg: Message):
    try:
        await msg.react(choice(Telegram.EMOJIS))
    except (MessageIdInvalid, EmoticonInvalid, ChatAdminRequired, ReactionInvalid):
        pass

# Telegram Bot Configuration
class Telegram:
    API_ID = int(env.get("TG_API_ID", "16457832"))
    API_HASH = env.get("TG_API_HASH", "3030874d0befdb5d05597deacc3e83ab")
    BOT_TOKEN = env.get("TG_BOT_TOKEN", "7939204796:AAGT3x8mqEKeM1yKIiS36L66P51vJq38Efs")
    BOT_USERNAME = env.get("TG_BOT_USERNAME", "DrReactBot")
    EMOJIS = [
        "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢",
        "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", 
        "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", 
        "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", 
        "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", 
        "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"
    ]

# Bot Client Initialization
version = 0.3
logger = getLogger('bot')

TelegramBot = Client(
    name="bot",
    api_id=Telegram.API_ID,
    api_hash=Telegram.API_HASH,
    bot_token=Telegram.BOT_TOKEN
)

if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.run()
