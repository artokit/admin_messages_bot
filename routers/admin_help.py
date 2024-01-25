from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
import db_api
from settings import ADMIN_GROUP_ID
from states import AdminHelp

router = Router()


@router.message(AdminHelp.message_to_admin)
async def admin_messages(message: Message):
    user = db_api.get_user(message.chat.id)
    await message.forward(ADMIN_GROUP_ID, user[1])


@router.message()
async def admin_answer(message: Message):
    if message.chat.id == int(ADMIN_GROUP_ID):
        user = db_api.get_user_by_thread_id(message.message_thread_id)

        try:
            await message.copy_to(user[0])
        except TelegramBadRequest:
            pass
