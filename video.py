import requests
import aria2p
from datetime import datetime
from status import format_progress_bar
import asyncio
import os
import time
import logging
from pyrogram.errors import MessageNotModified, RPCError

# Setup Aria2 connection
aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

# Download video function
async def download_video(url, reply_msg, user_mention, user_id):
    try:
        response = requests.get(f"https://test-api.gaurav281833.workers.dev/api?url={url}")
        response.raise_for_status()
        data = response.json()

        if "files" not in data or not data["files"]:
            raise Exception("No downloadable file found in API response.")

        file_info = data["files"][0]
        fast_download_link = file_info["download_link"]
        thumbnail_url = file_info["thumbnail"]
        video_title = file_info["file_name"]

        download = aria2.add_uris([fast_download_link])
        start_time = datetime.now()

        while not download.is_complete:
            download.update()
            percentage = download.progress
            done = download.completed_length
            total_size = download.total_length
            speed = download.download_speed
            eta = download.eta
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()

            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=done,
                total_size=total_size,
                status="Downloading",
                eta=eta,
                speed=speed,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=download.gid
            )

            try:
                await reply_msg.edit_text(progress_text)
            except MessageNotModified:
                pass
            await asyncio.sleep(2)

        if download.is_complete:
            file_path = download.files[0].path

            thumbnail_path = "thumbnail.jpg"
            try:
                thumbnail_response = requests.get(thumbnail_url)
                with open(thumbnail_path, "wb") as thumb_file:
                    thumb_file.write(thumbnail_response.content)
            except Exception as e:
                logging.warning(f"Thumbnail download failed: {e}")
                thumbnail_path = None

            try:
                await reply_msg.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ...")
            except MessageNotModified:
                pass

            return file_path, thumbnail_path, video_title
        else:
            raise Exception("Download failed")

    except Exception as e:
        logging.error(f"Download error: {e}")
        raise


# Upload video directly to user
async def upload_video(client, file_path, thumbnail_path, video_title, reply_msg, user_mention, user_id, message):
    file_size = os.path.getsize(file_path)
    uploaded = 0
    start_time = datetime.now()
    last_update_time = time.time()

    async def progress(current, total):
        nonlocal uploaded, last_update_time
        uploaded = current
        percentage = (current / total) * 100
        elapsed_time_seconds = (datetime.now() - start_time).total_seconds()

        if time.time() - last_update_time > 2:
            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=current,
                total_size=total,
                status="Uploading",
                eta=(total - current) / (current / elapsed_time_seconds) if current > 0 else 0,
                speed=current / elapsed_time_seconds if current > 0 else 0,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=""
            )
            try:
                await reply_msg.edit_text(progress_text)
                last_update_time = time.time()
            except MessageNotModified:
                pass
            except Exception as e:
                logging.warning(f"Progress edit error: {e}")

    try:
        with open(file_path, 'rb') as file:
            await client.send_video(
                chat_id=message.chat.id,
                video=file,
                caption=f"✨ {video_title}\n👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : {user_mention}\n📥 ᴜsᴇʀ ʟɪɴᴋ: tg://user?id={user_id}",
                thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                progress=progress
            )

        await asyncio.sleep(1)
        await message.delete()
        await message.reply_sticker("CAACAgIAAxkBAAEZdwRmJhCNfFRnXwR_lVKU1L9F3qzbtAAC4gUAAj-VzApzZV-v3phk4DQE")

    except RPCError as e:
        logging.error(f"Telegram upload failed: {e}")
        raise Exception("Failed to upload to Telegram.")

    finally:
        try:
            await reply_msg.delete()
        except Exception as e:
            logging.warning(f"Failed to delete reply_msg: {e}")

        try:
            os.remove(file_path)
        except Exception as e:
            logging.warning(f"Failed to delete file: {e}")

        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                os.remove(thumbnail_path)
            except Exception as e:
                logging.warning(f"Failed to delete thumbnail: {e}")
