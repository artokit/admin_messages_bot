import os
from aiogram import Bot
from aiogram.types import FSInputFile

HASH_DATA = {

}
MEDIA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')


async def send_video(video_name: str, bot: Bot, **kwargs):
    if video_name not in HASH_DATA:
        message = await bot.send_video(video=FSInputFile(os.path.join(MEDIA_PATH, video_name)), **kwargs)
        HASH_DATA[video_name] = message.video.file_id
        return message
    else:
        return await bot.send_video(video=HASH_DATA[video_name], **kwargs)
