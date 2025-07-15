import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ======== CONFIG ========
API_ID = 123456  # your api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
SESSION_STRING = "your_telethon_session_string"
ADMINS = [123456789]  # admin user IDs
BACKUP_CHANNEL = "@your_backup_channel"
# =========================

# Pyrogram bot client
bot = Client("stream_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Telethon client (user session)
user = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Global dict to store latest discwaal reply
discwaal_reply = {}

# Listen for reply from discwaal_bot
@user.on(events.NewMessage(from_users="discwaal_bot"))
async def handle_discwaal_reply(event):
    if "http" in event.raw_text:
        discwaal_reply["link"] = event.raw_text.strip()

# Send media to discwaal_bot and wait for stream link
async def send_to_discwaal(file_path: str):
    discwaal_reply.clear()
    await user.send_file("discwaal_bot", file_path)
    for _ in range(60):
        if "link" in discwaal_reply:
            return discwaal_reply["link"]
        await asyncio.sleep(1)
    return "\u26a0\ufe0f No response from @discwaal_bot"

# Get Telegram thumbnail (if available)
async def get_thumbnail(client, message: Message):
    if message.video and message.video.thumbs:
        return await client.download_media(message.video.thumbs[0].file_id)
    elif message.document and message.document.thumbs:
        return await client.download_media(message.document.thumbs[0].file_id)
    elif message.animation and message.animation.thumbs:
        return await client.download_media(message.animation.thumbs[0].file_id)
    return None

# Handle incoming media from admin
@bot.on_message(filters.private & filters.user(ADMINS))
async def handle_file(client: Client, message: Message):
    if not (message.video or message.animation or message.document):
        return

    if not user.is_connected():
        await user.start()

    status = await message.reply("\u23f3 Sending to @discwaal_bot...")

    try:
        file_path = await message.download()
        thumbnail = await get_thumbnail(client, message)
        stream_link = await send_to_discwaal(file_path)

        caption = (
            f"\ud83d\udcfb <b>Stream:</b> {stream_link}\n"
            f"\ud83d\udd01 <b>Join Backup Channel:</b> {BACKUP_CHANNEL}"
        )

        if thumbnail:
            await message.reply_photo(photo=thumbnail, caption=caption)
            os.remove(thumbnail)
        else:
            await message.reply_text(caption)

        os.remove(file_path)
        await status.delete()

    except Exception as e:
        print(f"\u274c Error: {e}")
        await status.edit("Something went wrong.")

# Start both clients together
async def main():
    await user.start()
    await bot.start()
    print("\u2705 Bot is running.")
    from pyrogram.idle import idle
    await idle()

asyncio.run(main())
