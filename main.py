from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from os.path import join, dirname
from utils.models import User, Compliment, AnonymousMessage
from utils.db import Database as db
from aiogram.filters import CommandStart, Filter
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import os
import asyncio
from aiogram.enums import ParseMode
from utils.keyboards import generate_keyboard_with_menu, generate_keyboard_with_users, generate_back_to_menu_button
from utils.states import SendAnonymousMessage
from sqlalchemy import func
from utils.message_type_sender import send_message_by_type
import re

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    with db.session() as session:
        user = session.query(User).filter(
            User.telegram_id==message.from_user.id
        ).first()

    if user:
        await message.answer(f"Снова привет, {message.from_user.first_name} 🙂", reply_markup=generate_keyboard_with_menu())
    else:
        new_user = User(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
        with db.session() as session:
            session.add(new_user)
            session.commit()
        await message.answer(f"Привет, {message.from_user.first_name}, вижу тебя впервые, добро пожаловать 🙂", reply_markup=generate_keyboard_with_menu())


@dp.message(F.text=="В главное меню")
async def go_to_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await start_command(message, state)


@dp.message(F.text=="Генератор комплиментов")
async def generate_compliment(message: Message, state: FSMContext) -> None:
    with db.session() as session:
        compliment = session.query(Compliment).order_by(func.random()).first()
    await message.answer(compliment.text, reply_markup=generate_keyboard_with_menu())


@dp.message(F.text=="Отправить анонимное сообщение")
async def choice_anonymous(message: Message, state: FSMContext) -> None:
    await state.set_state(SendAnonymousMessage.choice_user)
    await message.answer(f"Выберите из списка, кому хотите отправить анонимное сообщение (или если вам лень выбирать - напишите никнейм человека в формате @username) 🥰", reply_markup=generate_keyboard_with_users(message.from_user.id))
    

@dp.message(SendAnonymousMessage.choice_user)
async def choice_user_anonymous(message: Message, state: FSMContext) -> None:
    pattern = r'@(\w+)'
    match = re.findall(pattern, message.text)

    if match:
        with db.session() as session:
            user = session.query(User).filter(User.username==match[0]).first()

        if user:
            await state.update_data(user=user)
            await state.set_state(SendAnonymousMessage.generate_message)
            await message.answer("Что хотите отправить? (отправить можно текст, картинку, стикер, документ, голосовое или даже кружок) 🤗", reply_markup=generate_back_to_menu_button())
        else:
            await message.answer("Данный пользователь не найден в базе данных... я не могу написать пользователю, который не писал мне... выберите другого человека или вернитесь в главное меню 😔", reply_markup=generate_keyboard_with_users(message.from_user.id))

    else:
        await message.answer("Возможно вы допустили ошибку в никнейме пользователя, попробуйте ещё раз или вернитесь в главное меню 😔", reply_markup=generate_keyboard_with_users(message.from_user.id))


@dp.message(SendAnonymousMessage.generate_message)
async def generate_anonymous_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user = data.get('user')
    try:
        file_path, type = await send_message_by_type(bot, user.telegram_id, message, "Анонимный Валентин отправил вам сообщение:")
        download_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        anonymous_message = AnonymousMessage(sender_username=message.from_user.username, recipient_username=user.username, content=download_url, type=type)
        with db.session() as session:
            session.add(anonymous_message)
            session.commit()
        await message.answer('Сообщение отправлено 🥳', reply_markup=generate_keyboard_with_menu())
        await state.clear()
    except Exception as e:
        message.answer(e, reply_markup=generate_back_to_menu_button())

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    db.check_exists_db()
    asyncio.run(main())