import env
from Hack import bot
from Hack.helpers import MENU1, KEYBOARD1
from Hack.database import DB

from telethon import events


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    id = event.sender_id
    mention = f"[{event.sender.first_name}](tg://user?id={id})"
    TEXT = "Hey {}, I am a Session Hacker Bot Supporting Both Pyrogram and Telethon Session String. Type /hack to see menu"
    await event.reply(TEXT.format(mention))
    if DB:
        await DB.add_user(id)
    if env.LOG_GROUP_ID:
        await bot.send_message(env.LOG_GROUP_ID,
                               f'{mention} Has Just Started The Bot')


@bot.on(events.NewMessage(pattern="/hack"))
async def hack(event):
    if not event.is_private:
        return await event.reply("You can't use me in groups.")
    await event.reply(MENU1, buttons=KEYBOARD1)
