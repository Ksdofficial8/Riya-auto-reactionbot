from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageIdInvalid, ChatAdminRequired, EmoticonInvalid, ReactionInvalid
from random import choice
from bot import TelegramBot, logger
from bot.config import Telegram
from bot.modules.static import *
from logging import getLogger
from logging.config import dictConfig
from os import environ as env

# Logger Configuration
dictConfig(LOGGER_CONFIG_JSON)

# Emojis Text
SupportedEmojisText = """
**I currently support following emojis:**
""" + '\n'.join(' '.join(Telegram.EMOJIS[i:i+5]) for i in range(0, len(Telegram.EMOJIS), 5))

# Command Handlers
@TelegramBot.on_message(filters.command('start') & (filters.private | filters.group))
async def start_command(_, msg: Message):
    return await msg.reply(
        text=WelcomeText % {'first_name': msg.from_user.first_name if msg.from_user else 'Anonymous'},
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Add me to chat', url=f'https://t.me/{Telegram.BOT_USERNAME}?startgroup=botstart')],
            [InlineKeyboardButton(text='Source Code', url='https://github.com/TheCaduceus/TG-ReactionBot')]
        ])
    )

@TelegramBot.on_message(filters.command('emojis') & (filters.private | filters.group))
async def send_emojis(_, msg: Message):
    return await msg.reply(
        text=SupportedEmojisText,
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Reference', url='https://github.com/TheCaduceus/TG-ReactionBot/blob/main/bot/config.py#L8')]
        ])
    )

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
    bot_token=Telegram.BOT_TOKEN,
    plugins={'root': 'bot/plugins'}
)

if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.run()
