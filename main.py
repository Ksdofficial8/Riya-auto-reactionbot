import os
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import MessageIdInvalid, ChatAdminRequired, EmoticonInvalid, ReactionInvalid
from random import choice
from pyrogram import Client
from logging import getLogger
from logging.config import dictConfig
from pymongo import MongoClient  # Import MongoDB client

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
API_ID = int(os.getenv("TG_API_ID", "16457832"))
API_HASH = os.getenv("TG_API_HASH", "3030874d0befdb5d05597deacc3e83ab")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "7638229482:AAECDi3SkCa9KTE-YaC3B5fzJ7a9HL6IYEU")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME", "DrReactBot")

# List of emojis
EMOJIS = [
    "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", 
    "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", 
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", 
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"
]

# MongoDB setup (make sure your MongoDB instance is running)
mongo_client = MongoClient('mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority')  # Update with your MongoDB URI if necessary
db = mongo_client['bot_db']  # Database name
reactions_collection = db['reactions']  # Collection to store reaction status

# Create the Telegram bot client
TelegramBot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Function to get the current reaction status from MongoDB
def get_reaction_status():
    status = reactions_collection.find_one({"_id": "reaction_status"})
    return status["enabled"] if status else False

# Function to set the reaction status in MongoDB
def set_reaction_status(enabled: bool):
    reactions_collection.update_one(
        {"_id": "reaction_status"},
        {"$set": {"enabled": enabled}},
        upsert=True
    )

# Command to turn reactions on
@TelegramBot.on_message(filters.command("reaction on"))
async def reaction_on(_, msg: Message):
    set_reaction_status(True)
    await msg.reply("𓌉◯𓇋 Rᴇᴀᴄᴛɪᴏɴ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠɪᴛᴇᴅ ✅")

# Command to turn reactions off
@TelegramBot.on_message(filters.command("reaction off"))
async def reaction_off(_, msg: Message):
    set_reaction_status(False)
    await msg.reply("𓌉◯𓇋 Rᴇᴀᴄᴛɪᴏɴ ᴍᴏᴅᴇ ᴅᴇᴀᴄᴛɪᴠɪᴛᴇᴅ ❌")

# Command to guide the user when they enter `/reaction` and show current status
@TelegramBot.on_message(filters.command("reaction"))
async def guide_reaction(_, msg: Message):
    # Get the current reaction status
    status = get_reaction_status()
    status_message = "enabled" if status else "disabled"
    await msg.reply(f"Reactions are currently {status_message}.\n\nTo enable reactions, type `/reaction on`. To disable reactions, type `/reaction off`.")

# Define message reaction logic
@TelegramBot.on_message(filters.all)
async def send_reaction(_, msg: Message):
    # Check if reactions are enabled
    if get_reaction_status():
        try:
            await msg.react(choice(EMOJIS))
        except (MessageIdInvalid, EmoticonInvalid, ChatAdminRequired, ReactionInvalid):
            pass

# Start the bot
if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.run()
