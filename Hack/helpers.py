import base64
import struct
import asyncio
import ipaddress
import requests as r

from Hack import bot
from logger import LOGGER
from traceback import format_exc
from env import LOG_GROUP_ID, MUST_JOIN, DISABLED

from telethon import errors, Button
from telethon.events import CallbackQuery
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession
from telethon.errors.rpcerrorlist import UserNotParticipantError, UserIsBlockedError


MENU1 = '''
𝗔 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝗼𝘄𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝗮𝗻𝗱 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀(𝗣𝗨𝗕𝗟𝗜𝗖 𝗢𝗡𝗟𝗬)

𝗕 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝗮𝗹𝗹 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗹𝗶𝗸𝗲 𝗽𝗵𝗼𝗻𝗲 𝗻𝘂𝗺𝗯𝗲𝗿, 𝘂𝘀𝗿𝗻𝗮𝗺𝗲... 𝗲𝘁𝗰

𝗖 - 𝗕𝗮𝗻 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗺𝗲𝗺𝗯𝗲𝗿𝘀 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽

𝗗 - 𝗞𝗻𝗼𝘄 𝘂𝘀𝗲𝗿 𝗹𝗮𝘀𝘁 𝗼𝘁𝗽, 𝗨𝘀𝗲 𝗼𝗽𝘁𝗶𝗼𝗻 𝗕 𝗳𝗶𝗿𝘀𝘁 𝘁𝗼 𝘁𝗮𝗸𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝘁𝗵𝗲𝗻 𝗹𝗼𝗴𝗶𝗻

𝗘 - 𝗝𝗼𝗶𝗻 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹/𝗟𝗶𝗻𝗸 𝘃𝗶𝗮 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗙 - 𝗟𝗲𝗮𝘃𝗲 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘃𝗶𝗮 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗚 - 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹

𝗛 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝘁𝘄𝗼 𝘀𝘁𝗲𝗽 𝗶𝘀 𝗲𝗻𝗲𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲
'''

MENU2 = '''
𝗜 - 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝘁𝗲 𝗔𝗹𝗹 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗮𝗰𝘁𝗶𝘃𝗲 𝘀𝗲𝘀𝘀𝗶𝗼𝗻𝘀 𝗲𝘅𝗰𝗲𝗽𝘁 𝗬𝗼𝘂𝗿 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗝 - 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔𝗰𝗰𝗼𝘂𝗻𝘁

𝗞 - 𝗟𝗲𝗮𝘃𝗲 𝗔𝗹𝗹 𝗚𝗿𝗼𝘂𝗽𝘀/𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀

𝗟 - 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗕𝘂𝘁𝘁𝗼𝗻𝘀

𝗠 - 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝘁𝗲 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗡 - 𝗜𝗻𝘃𝗶𝘁𝗲 𝗔𝗹𝗹

𝗢 - 𝗗𝗲𝗺𝗼𝘁𝗲 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿

𝗣 - 𝗣𝗿𝗼𝗺𝗼𝘁𝗲 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿
'''

BROADCAST_BUTTONS = [[
    Button.inline("Group", data="1"),
    Button.inline("User", data="2"),
], [
    Button.inline("All", data="3"),
]]

BROADCAST_OPTION = {
    b"1": {
        "group": True
    },
    b"2": {
        "user": True
    },
    b"3": {
        "group": True,
        "user": True
    }
}

KEYBOARD1 = [
    [
        Button.inline("A", data="A"),
        Button.inline("B", data="B"),
        Button.inline("C", data="C"),
        Button.inline("D", data="D")
    ],
    [
        Button.inline("E", data="E"),
        Button.inline("F", data="F"),
        Button.inline("G", data="G"),
        Button.inline("H", data="H")
    ],
    [
        Button.inline("𝗡𝗘𝗫𝗧 ⏭️", data="next")
    ]
]

KEYBOARD2 = [
    [
        Button.inline("I", data="I"),
        Button.inline("J", data="J"),
        Button.inline("K", data="K"),
        Button.inline("L", data="L")
    ],
    [
        Button.inline("M", data="M"),
        Button.inline("N", data="N"),
        Button.inline("O", data="O"),
        Button.inline("P", data="P")
    ],
    [
        Button.inline(" 𝗕𝗔𝗖𝗞 ⏮️", data="back")
    ]
]


async def join_checker(e):
    if not MUST_JOIN:
        return True
    chat = await bot.get_entity(MUST_JOIN)
    try:
        await bot(GetParticipantRequest(chat, e.sender_id))
        return True
    except UserNotParticipantError:
        join_chat = f"https://t.me/{chat.username}"
        button = [[
            Button.url(text="Join", url=join_chat),
        ]]

        TEXT = "Hey looks like you haven't join our chat yet, Please join first!"

        await bot.send_message(e.sender_id, TEXT, buttons=button)

        return False
    except Exception as err:
        LOGGER(__name__).error(err)
        return True


def paste(text):
    link = 'https://spaceb.in/'
    url = 'https://spaceb.in/api/v1/documents'
    payload = {"content": text, "extension": "txt"}
    headers = {
        "Content-Type": "application/json"
    }

    response = r.post(url, json=payload, headers=headers)
    hash = response.json().get('payload').get('id')

    return link + hash


def on_callback(data=None):
    def dec(func):
        async def wrap(e):
            check = await join_checker(e)
            if not check:
                return

            if func.__name__ in DISABLED:
                await e.answer("This function is currently disabled", alert=True)
                return
            try:
                await func(e)
            except errors.common.AlreadyInConversationError:
                pass
            except (asyncio.CancelledError, UserIsBlockedError):
                return
            except Exception as err:
                ERROR_TXT = f'ERROR MESSAGE:- {err}'
                ERROR_TXT += f'\n\nERROR TRACEBACK:- {format_exc()}'
                if LOG_GROUP_ID:
                    try:
                        link = paste(ERROR_TXT)
                        await bot.send_message(LOG_GROUP_ID, link, link_preview=False)
                    except:
                        pass
                else:
                    LOGGER(__name__).error(ERROR_TXT)
                await e.reply('Some Error occur from bot side. Please report it to @MASTIWITHFRIENDSXD')

        bot.add_event_handler(wrap, CallbackQuery(data=data))

    return dec



# https://github.com/TeamUltroid/Ultroid/blob/main/pyUltroid/startup/connections.py

_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def validate_session(session):
    # Telethon Session
    if session.startswith(CURRENT_VERSION):
        if len(session.strip()) != 353:
            return False
        return StringSession(session)

    # Pyrogram Session
    elif len(session) in _PYRO_FORM.keys():
        if len(session) in [351, 356]:
            dc_id, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        else:
            dc_id, _, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        return StringSession(CURRENT_VERSION + base64.urlsafe_b64encode(
            struct.pack(
                _STRUCT_PREFORMAT.format(4),
                dc_id,
                ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                443,
                auth_key,
            )).decode("ascii"))
    else:
        return False
