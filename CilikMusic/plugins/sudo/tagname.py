#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from CilikMusic import app
from CilikMusic.misc import MENTION
from CilikMusic.utils.database import add_mentions, remove_mentions
from CilikMusic.utils.decorators.tools import get_arg

# Command



@app.on_message(
    filters.command("addmentions", [".", "-", "^", "!", "/"]) & filters.user(OWNER_ID)
)
async def addmen(client, message: Message):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**Due to bot's privacy issues, You can't manage sudo users when you're using Cilik's Database.\n\n Please fill your MONGO_DB_URI in your vars to use this feature**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("ℹ️ Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in MENTION:
            return await message.reply_text(
                "{} sudah masuk di list mention".format(user.mention)
            )
        added = await add_mentions(user.id)
        if added:
            MENTION.add(user.id)
            await message.reply_text("➕ Ditambahkan {} ke List Mentions".format(user.mention))
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in MENTION:
        return await message.reply_text(
            "{} sudah masuk di list mention".format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_mentions(message.reply_to_message.from_user.id)
    if added:
        MENTION.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            "➕ Ditambahkan {} ke List Mentions".format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("Failed")
    return


@app.on_message(
    filters.command("delmentions", [".", "-", "^", "!", "/"]) & filters.user(OWNER_ID)
)
async def delmen(client, message: Message):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**Due to bot's privacy issues, You can't manage sudo users when you're using Cilik's Database.\n\n Please fill your MONGO_DB_URI in your vars to use this feature**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("ℹ️ Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in MENTION:
            return await message.reply_text("Bukan bagian dari List Mentions")
        removed = await remove_mentions(user.id)
        if removed:
            MENTION.remove(user.id)
            await message.reply_text("🚮 Dihapus dari List Mentions")
            return
        await message.reply_text(f"Something wrong happened.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in MENTION:
        return await message.reply_text("Bukan bagian dari List Mentions")
    removed = await remove_mentions(user_id)
    if removed:
        MENTION.remove(user_id)
        await message.reply_text("🚮 Dihapus dari List Mentions")
        return
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command("mentions", [".", "-", "^", "!", "/"]) & ~BANNED_USERS)
async def list_men(client, message: Message):
    if message.reply_to_message or get_arg(message):
        return await message.reply("Berikan Sebuah Text atau Reply")
    elif:
        mode = "text_on_reply"
        text = message.reply_to_message
    elif:
        mode = "text_on_cmd"
        text = get_arg(message)

    for user_id in MENTION:
        user = await app.get_users(user_id)
        user = (
            user.first_name
            if not user.mention
            else user.mention
            )
        usrnum += 1
        usrtxt += f"{user} "
        if usrnum == 50:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n{text}"
                await app.send_message(message.chat.id, txt)
            elif mode == "text_on_reply":
                await text.reply(usrtxt)    
