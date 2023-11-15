import env
import asyncio
from Hack import bot
from Hack.database import DB

from telethon import events, errors


@bot.on(events.NewMessage(pattern=r"/broadcast\s*([\s\S]*)?"))
async def broadcast(event):
    if not DB:
        await event.reply('Add Mongo Url First')
        return
    if not (event.sender_id in env.SUDOERS):
        return
    text = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not (text or reply):
        return await event.reply('Please Give A Text Or Reply To a Message')
    sent = 0
    ids = await DB.get_users()

    msg = await event.reply(
        "**Processing....\nPlease Dont Delete The Replied Message**"
    ) if reply else await event.reply('**Processing....**')
    for user in ids:
        try:
            await reply.forward_to(user) if reply else await bot.send_message(
                user, text)
            sent += 1
            await asyncio.sleep(0.8)
        except errors.rpcerrorlist.FloodWaitError as fwerr:
            await asyncio.sleep(fwerr.seconds + 5)
        except Exception:
            continue

    result = f"**Broadcasted In {len(ids)} Chats **"
    try:
        await msg.edit(result)
    except:
        await event.reply(result)
