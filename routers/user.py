import asyncio
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, ChatJoinRequest, ChatMemberUpdated
import db_api
from settings import ADMIN_GROUP_ID
from states import AutoMessages, AdminHelp
from bot_functions import hashed_media
storage = None
CHAT_ID = -1002135411554

router = Router()

async def create_forum_topic(user_id: int, bot: Bot, name: str):
    user = db_api.get_user(user_id)
    if user:
        if not user[1]:
            m = await bot.create_forum_topic(ADMIN_GROUP_ID, name)
            db_api.set_thread_id(user_id, m.message_thread_id)

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not db_api.add_user(message.chat.id):
        await state.set_state(AdminHelp.message_to_admin)
        return
    
    await create_forum_topic(message.chat.id, message.bot, message.chat.username or str(message.chat.id))
    # m = await message.bot.create_forum_topic(ADMIN_GROUP_ID, message.chat.username or str(message.chat.id))
    # db_api.set_thread_id(message.chat.id, m.message_thread_id)

    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(20)
    user = db_api.get_user(message.chat.id)
    print(user)
    if not await state.get_state():
        msg = await message.answer("🔥Hola. Quieres que te enseñe a ganar dinero con Aviator?🔥")
        await msg.forward(ADMIN_GROUP_ID, user[1])
        await state.set_state(AutoMessages.ask_want_earn)

    await asyncio.sleep(30)

    if await state.get_state() == AutoMessages.ask_want_earn:
        await answer_earn(message, state)

    await asyncio.sleep(180)

    if await state.get_state() == AutoMessages.ask_to_join:
        await answer_to_join(message, state)


@router.message(AutoMessages.ask_want_earn)
async def answer_earn(message: Message, state: FSMContext):
    user = db_api.get_user(message.chat.id)
    await message.forward(ADMIN_GROUP_ID, user[1])
    await state.set_state(AutoMessages.ask_to_join)
    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(10)

    msg = await hashed_media.send_video(
        'video1.mp4',
        message.bot,
        chat_id=message.chat.id,
        caption="🤩Mírame ganar dinero con el juego Aviador con los chicos.🤩\n"
                "💰Los chicos de mi equipo están haciendo $100-$200 al día mínimo.\n"
                "Listo para formar y unirse a mi equipo?"
    )

    await msg.forward(ADMIN_GROUP_ID, user[1])
    await state.set_state(AutoMessages.ask_to_join)


async def answer_earn_id(user_id: int, bot: Bot, state: FSMContext):
    await state.set_state(AutoMessages.ask_to_join)
    await asyncio.sleep(5)
    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(10)

    msg = await hashed_media.send_video(
        'video1.mp4',
        bot,
        chat_id=user_id,
        caption="🤩Mírame ganar dinero con el juego Aviador con los chicos.🤩\n"
                "💰Los chicos de mi equipo están haciendo $100-$200 al día mínimo.\n"
                "Listo para formar y unirse a mi equipo?"
    )

    user = db_api.get_user(user_id)
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await state.set_state(AutoMessages.ask_to_join)


@router.message(AutoMessages.ask_to_join)
async def answer_to_join(message: Message, state: FSMContext):
    user = db_api.get_user(message.chat.id)
    await message.forward(ADMIN_GROUP_ID, user[1])
    await state.set_state(AdminHelp.message_to_admin)
    await asyncio.sleep(5)
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(15)

    msg = await hashed_media.send_video(
        'video2.mp4',
        message.bot,
        chat_id=message.chat.id,
        caption="🔥 Aquí es donde vamos a ganar dinero, ahora registrar una nueva cuenta en este sitio :"
                " https://1wcdcw.xyz/casino/list?open=register#r53b .\n"
                "Asegúrate de tener una cuenta nueva, ya que mis señales sólo funcionan con cuentas nuevas a través "
                "de mi enlace\n"
                "Después de eso envíame un correo electrónico e iremos al siguiente paso, ¿puedes hacerlo ahora?"
    )

    await msg.forward(ADMIN_GROUP_ID, user[1])

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)

    msg = await message.answer("💰Código promocional: AVIATORAXEL")
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)

    msg = await message.answer("❗️❗️Con cuentas antiguas mis estrategias no funcionan ❗️❗️")
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)

    msg = await message.answer(
        "Hay dos formas de registrarse en el sitio:\n" 
        "1) A través del número de teléfono, correo.\n"
        "2) A través de las redes sociales"
    )

    await msg.forward(ADMIN_GROUP_ID, user[1])

    await message.bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(5)

    msg = await message.answer("Si necesitas ayuda - He adjuntado una guía de vídeo sobre cómo sign up.🤓")
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await create_forum_topic(message.chat.id, message.bot, message.chat.username or str(message.chat.id))
    # m = await message.bot.create_forum_topic(ADMIN_GROUP_ID, message.chat.username or str(message.chat.id))
    # db_api.set_thread_id(message.chat.id, m.message_thread_id)
    await state.clear()


async def answer_to_join_id(user_id: int, bot: Bot, state: FSMContext, username: str):
    user = db_api.get_user(user_id)
    await state.set_state(AdminHelp.message_to_admin)
    await asyncio.sleep(5)
    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(15)

    msg = await hashed_media.send_video(
        'video2.mp4',
        bot,
        chat_id=user_id,
        caption="🔥 Aquí es donde vamos a ganar dinero, ahora registrar una nueva cuenta en este sitio :"
                " https://1wcdcw.xyz/casino/list?open=register#r53b .\n"
                "Asegúrate de tener una cuenta nueva, ya que mis señales sólo funcionan con cuentas nuevas a través "
                "de mi enlace\n"
                "Después de eso envíame un correo electrónico e iremos al siguiente paso, ¿puedes hacerlo ahora?"
    )
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(5)
    # msg = await bot.send_message("
    # msg = await bot.send_message("
    # msg = await bot.send_message("
    msg = await bot.send_message(user_id, "💰Código promocional: AVIATORAXEL")
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(5)
    msg = await bot.send_message(user_id, "❗️❗️Con cuentas antiguas mis estrategias no funcionan ❗️❗️")
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(5)
    msg = await bot.send_message(
        user_id,
        "Hay dos formas de registrarse en el sitio:\n" 
        "1) A través del número de teléfono, correo.\n"
        "2) A través de las redes sociales"
    )
    await msg.forward(ADMIN_GROUP_ID, user[1])

    await bot.send_chat_action(user_id, action="typing")
    await asyncio.sleep(5)
    msg = await bot.send_message(user_id, "Si necesitas ayuda - He adjuntado una guía de vídeo sobre cómo sign up.🤓")
    await msg.forward(ADMIN_GROUP_ID, user[1])
    await state.clear()
   #  m = await bot.create_forum_topic(ADMIN_GROUP_ID, username or str(user_id))
   #  db_api.set_thread_id(user_id, m.message_thread_id)


@router.chat_join_request()
async def start1(update: ChatJoinRequest):
    state = FSMContext(
        storage=storage,  # dp - экземпляр диспатчера
        key=StorageKey(
            chat_id=update.from_user.id,  # если юзер в ЛС, то chat_id=user_id
            bot_id=update.bot.id, user_id=update.from_user.id))

    if not db_api.add_user(update.from_user.id):
        await state.set_state(AdminHelp.message_to_admin)
        return

    await create_forum_topic(update.from_user.id, update.bot, update.from_user.username or str(update.from_user.id))
    # m = await update.bot.create_forum_topic(ADMIN_GROUP_ID, update.from_user.username or str(update.from_user.id))
    # db_api.set_thread_id(update.from_user.id, m.message_thread_id)

    # db_api.add_user(update.chat.id)
    # global storage
    # m = await update.bot.create_forum_topic(ADMIN_GROUP_ID, update.chat.username or str(update.from_user.id))
    # print(m.message_thread_id)
    # db_api.set_thread_id(update.from_user.id, m.message_thread_id)

    # await asyncio.sleep(60)
    await update.approve()

    # state = FSMContext(
    #     storage=storage,  # dp - экземпляр диспатчера
    #     key=StorageKey(
    #         chat_id=update.from_user.id,  # если юзер в ЛС, то chat_id=user_id
    #         bot_id=update.bot.id, user_id=update.from_user.id))

    # if not db_api.add_user(update.from_user.id):
    #     await state.set_state(AdminHelp.message_to_admin)
    #     return

    user = db_api.get_user(update.from_user.id)
    print(user)
    await asyncio.sleep(5)
    await update.bot.send_chat_action(update.from_user.id, action="typing")
    await asyncio.sleep(20)

    if not await state.get_state():
        msg = await update.bot.send_message(update.from_user.id, "🔥Hola. Quieres que te enseñe a ganar dinero con Aviator?🔥")
        await msg.forward(ADMIN_GROUP_ID, user[1])
        await state.set_state(AutoMessages.ask_want_earn)

    await asyncio.sleep(30)

    if await state.get_state() == AutoMessages.ask_want_earn:
        await answer_earn_id(user_id=update.from_user.id, bot=update.bot, state=state)

    await asyncio.sleep(180)

    if await state.get_state() == AutoMessages.ask_to_join:
        await answer_to_join_id(update.from_user.id, update.bot, state, update.from_user.username)
    
    # await state.set_state(AdminHelp.message_to_admin)


@router.chat_member()
async def test_chat_member(chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member.status == 'left':
        user = db_api.get_user(chat_member_updated.from_user.id)
        await chat_member_updated.bot.send_message(
            chat_member_updated.from_user.id,
            f"""¡No pierdas la oportunidad de ganar todo conmigo! 🚀 ¡Siempre puedes escribir y yo te ayudaré! 🤑"""
        )

        await chat_member_updated.bot.send_message(ADMIN_GROUP_ID, "ВЫШЕЛ ИЗ КАНАЛА!", message_thread_id=user[1])


