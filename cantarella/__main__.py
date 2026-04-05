#@cantarellabots
import sys
import asyncio
import logging
import pyrogram.utils
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN
from cantarella.telegram.ongoing import ongoing_task

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("Please set API_ID, API_HASH, and BOT_TOKEN environment variables.")
    sys.exit(1)

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

app = Client(
    "anime_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="cantarella.telegram.plugins"),
    workers=100,
    parse_mode=ParseMode.HTML
)

if __name__ == "__main__":
    print("Aniwatchtv downloader Bot started")

    async def main():
        await app.start()

        # Check for restart message to update
        try:
            from cantarella.core.database import db
            from config import OWNER_ID
            restart_msg_id = await db.get_user_setting(OWNER_ID, "restart_msg_id")
            restart_chat_id = await db.get_user_setting(OWNER_ID, "restart_chat_id")
            if restart_msg_id and restart_chat_id:
                try:
                    await app.edit_message_text(
                        chat_id=restart_chat_id,
                        message_id=restart_msg_id,
                        text="<b>✅ ʙᴏᴛ ʀᴇꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b>",
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    logging.error(f"Failed to edit restart message: {e}")
                # Clear the settings
                await db.set_user_setting(OWNER_ID, "restart_msg_id", None)
                await db.set_user_setting(OWNER_ID, "restart_chat_id", None)
        except Exception as e:
            logging.error(f"Error checking restart status: {e}")
        asyncio.create_task(ongoing_task(app))
        import pyrogram
        await pyrogram.idle()
        await app.stop()

    # Get the existing event loop to avoid cross-loop Future errors in Pyrogram executor
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
