from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import settings
import asyncio
from routers import user, admin_help


async def run():
    s = MemoryStorage()
    dp = Dispatcher(storage=s)
    user.storage = s
    bot = Bot(settings.TOKEN)
    dp.include_routers(user.router, admin_help.router)
    await dp.start_polling(bot)


asyncio.run(run())
