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
    filters.command("addmentions", [".", "-", "!", "^", "/"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
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
    filters.command("delmentions", [".", "-", "!", "^", "/"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
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


  
@app.on_message(
    filters.command(["mentions", "daget"], [".", "-", "!", "^", "/"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
async def men_list(client, message: Message):
    rep = message.reply_to_message
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not rep and not msg:
        return await message.reply("**Usage:**\n/mentions {text}")
    text = " "
    count = 0
    smex = 0
    for user_id in MENTION:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if smex == 0:
                    smex += 1
                    text += " "
                count += 1
                text += f", {user}" 
            except Exception:
                continue
    if not text:
        await message.reply_text("Tidak ada user yang di mentions")
    else:
        yy = await message.reply_text(text)
    if msg:
        text += f"\n\n{msg}"
    await yy.edit(text)
        
