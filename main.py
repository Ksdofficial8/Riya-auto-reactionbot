import os  # You need to import os to access environment variables
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import MessageIdInvalid, ChatAdminRequired, EmoticonInvalid, ReactionInvalid 
from random import choice
from pyrogram import Client
from logging import getLogger
from logging.config import dictConfig

# Logger configuration remains the same
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

dictConfig(LOGGER_CONFIG_JSON)

version = 0.3
logger = getLogger('bot')

# Set your environment variables here or load them from your system's environment
API_ID = int(os.getenv("TG_API_ID", "16457832"))  # Replace default value with your own
API_HASH = os.getenv("TG_API_HASH", "3030874d0befdb5d05597deacc3e83ab")  # Replace default value with your own
BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "8081146945:AAG-E_dfYgV_reJXx3jSdaGoac-NSfzDZpY")  # Replace with actual bot token
BOT_USERNAME = os.getenv("TG_BOT_USERNAME", "DrReactBot")

# List of emojis
EMOJIS = [
    "👍", "👎", "❤", "🔥", 
    "🥰", "👏", "😁", "🤔",
    "🤯", "😱", "🤬", "😢",
    "🎉", "🤩", "🤮", "💩",
    "🙏", "👌", "🕊", "🤡",
    "🥱", "🥴", "😍", "🐳",
    "❤‍🔥", "🌚", "🌭", "💯",
    "🤣", "⚡", "🍌", "🏆",
    "💔", "🤨", "😐", "🍓",
    "🍾", "💋", "🖕", "😈",
    "😴", "😭", "🤓", "👻",
    "👨‍💻", "👀", "🎃", "🙈",
    "😇", "😨", "🤝", "✍",
    "🤗", "🫡", "🎅", "🎄",
    "☃", "💅", "🤪", "🗿",
    "🆒", "💘", "🙉", "🦄",
    "😘", "💊", "🙊", "😎",
    "👾", "🤷‍♂", "🤷", "🤷‍♀",
    "😡"
]

# Create the Telegram bot client
TelegramBot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define message reaction logic
@TelegramBot.on_message(filters.all)
async def send_reaction(_, msg: Message):
    try:
        await msg.react(choice(EMOJIS))
    except (
        MessageIdInvalid,
        EmoticonInvalid,
        ChatAdminRequired,
        ReactionInvalid
    ):
        pass

# Start the bot
if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.run()
