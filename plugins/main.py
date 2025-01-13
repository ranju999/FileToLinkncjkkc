from pyrogram import Client, filters
from info import URL, BIN_CHANNEL
from utils import get_hash
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"**Hello {message.from_user.mention},\nI am a Telegram Video Stream Bot. Send me any video and I will give you streaming & download link.**")


@Client.on_message((filters.private) & (filters.document | filters.video) , group=4)
async def private_receive_handler(client, message):
    file_id = message.document or message.video

    msg = await message.copy(
        chat_id=BIN_CHANNEL,
        caption=f"**File Name:** {file_id.file_name}\n\n**Requested By:** {message.from_user.mention}")

    file_name = file_id.file_name.replace("_", " ").replace(".mp4", "").replace(".mkv", "").replace(".", " ")
    online = f"{URL}watch/{msg.id}?hash={get_hash(msg)}"
    download = f"{URL}download/{msg.id}?hash={get_hash(msg)}"

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
