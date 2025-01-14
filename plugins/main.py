import asyncio
from pyrogram import Client, filters
from info import URL, BIN_CHANNEL
from web.av import get_hash
from pyrogram.types import *
from pyrogram.errors import *

@Client.on_message((filters.private) & (filters.document | filters.video) , group=4)
async def private_receive_handler(client, message):
    file_id = message.document or message.video

    msg = await message.copy(
        chat_id=BIN_CHANNEL,
        caption=f"**File Name:** {file_id.file_name}\n\n**Requested By:** {message.from_user.mention}")

    file_name = file_id.file_name.replace("_", " ").replace(".mp4", "").replace(".mkv", "").replace(".", " ")
    online = f"{URL}watch/{msg.id}?hash={get_hash(msg)}"
    download = f"{URL}download/{msg.id}?hash={get_hash(msg)}"
    await message.delete()
    await message.reply_text(
        text=f"<b>Here Is Your Streamable Link\n\nFile Name</b>: - <a href=https://t.me/av_botz>{file_name}</a></b>",
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Watch", url=online),
                InlineKeyboardButton("Download", url=download)
            ]
        ]
    ),
    reply_to_message_id=message.id,
    disable_web_page_preview=True)

@Client.on_message((filters.private) & (filters.photo | filters.audio) , group=4)
async def photo_audio_erorr(client, message):
    await message.reply_text(f"**Dude! Send me a video file.**")

@Client.on_message(filters.channel & ~filters.group & (filters.document | filters.video)  & ~filters.forwarded, group=-1)
async def nel_receive_handler(bot, broadcast):
    try:
        msg = await broadcast.forward(chat_id=BIN_CHANNEL)
        online = f"{URL}watch/{msg.id}?hash={get_hash(msg)}"
        download = f"{URL}download/{msg.id}?hash={get_hash(msg)}"
        await msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {online}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("sᴛʀᴇᴀᴍ", url=online),
                    InlineKeyboardButton('ᴅᴏᴡɴʟᴏᴀᴅ', url=download)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=BIN_CHANNEL)
        
    except Exception as e:
        await bot.send_message(chat_id=BIN_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Channel!{e}**")

