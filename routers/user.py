import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import db_api
from settings import ADMIN_GROUP_ID
from states import AutoMessages, AdminHelp
from bot_functions import hashed_media

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not db_api.add_user(message.chat.id):
        await state.set_state(AdminHelp.message_to_admin)
        return

    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(20)

    if not await state.get_state():
        await message.answer("🔥Hola. Quieres que te enseñe a ganar dinero con Aviator?🔥")
        await state.set_state(AutoMessages.ask_want_earn)

    await asyncio.sleep(30)

    if await state.get_state() == AutoMessages.ask_want_earn:
        await answer_earn(message, state)

    await asyncio.sleep(180)

    if await state.get_state() == AutoMessages.ask_to_join:
        await answer_to_join(message, state)


@router.message(AutoMessages.ask_want_earn)
async def answer_earn(message: Message, state: FSMContext):
    await state.set_state(AutoMessages.ask_to_join)
    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(10)

    await hashed_media.send_video(
        'video1.mp4',
        message.bot,
        chat_id=message.chat.id,
        caption="🤩Mírame ganar dinero con el juego Aviador con los chicos.🤩\n"
                "💰Los chicos de mi equipo están haciendo $100-$200 al día mínimo.\n"
                "Listo para formar y unirse a mi equipo?"
    )
    await state.set_state(AutoMessages.ask_to_join)


@router.message(AutoMessages.ask_to_join)
async def answer_to_join(message: Message, state: FSMContext):
    await state.set_state(AdminHelp.message_to_admin)
    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(15)

    await hashed_media.send_video(
        'video2.mp4',
        message.bot,
        chat_id=message.chat.id,
        caption="🔥 Aquí es donde vamos a ganar dinero, ahora registrar una nueva cuenta en este sitio :"
                " https://1wauah.xyz/casino/list?open=register#r53b .\n"
                "Asegúrate de tener una cuenta nueva, ya que mis señales sólo funcionan con cuentas nuevas a través "
                "de mi enlace\n"
                "Después de eso envíame un correo electrónico e iremos al siguiente paso, ¿puedes hacerlo ahora?"
    )

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)
    await message.answer("💰Código promocional: AVIATORALEX")

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)
    await message.answer("❗️❗️Con cuentas antiguas mis estrategias no funcionan ❗️❗️")

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)
    await message.answer(
        "Hay dos formas de registrarse en el sitio:\n" 
        "1) A través del número de teléfono, correo.\n"
        "2) A través de las redes sociales"
    )

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)
    await message.answer("Si necesitas ayuda - He adjuntado una guía de vídeo sobre cómo sign up.🤓")

    m = await message.bot.create_forum_topic(ADMIN_GROUP_ID, message.chat.username or str(message.chat.id))
    db_api.set_thread_id(message.chat.id, m.message_thread_id)
