#
# Copyright (C) 2023-2024 by YukkiOwner@Github, < https://github.com/YukkiOwner >.
#
# This file is part of < https://github.com/YukkiOwner/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/YukkiOwner/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import set_cmode
from YukkiMusic.utils.decorators.admins import AdminActual

### Multi-Lang Commands
CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@app.on_message(
    filters.command(CHANNELPLAY_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            _["cplay_1"].format(
                message.chat.title, CHANNELPLAY_COMMAND[0]
            )
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("Channel Play Disabled")
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if not chat.linked_chat:
            return await message.reply_text(_["cplay_2"])
        chat_id = chat.linked_chat.id
        await set_cmode(message.chat.id, chat_id)
        return await message.reply_text(
            _["cplay_3"].format(
                chat.linked_chat.title, chat.linked_chat.id
            )
        )
    else:
        try:
            chat = await app.get_chat(query)
        except Exception as e:
            print(f"Error: {e}")
            return await message.reply_text(_["cplay_4"])
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(_["cplay_5"])
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    creatorusername = user.user.username
                    creatorid = user.user.id
        except Exception as e:
            print(f"Error: {e}")
            return await message.reply_text(_["cplay_4"])
        if creatorid != message.from_user.id:
            return await message.reply_text(
                _["cplay_6"].format(chat.title, creatorusername)
            )
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(
            _["cplay_3"].format(chat.title, chat.id)
        )
