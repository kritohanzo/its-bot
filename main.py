from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from os.path import join, dirname
from utils.models import User, Compliment
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
from utils.keyboards import generate_keyboard_with_menu, generate_keyboard_with_users
from utils.states import SendAnonymousMessage
from sqlalchemy import func

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
    await message.answer(f"Выбери, кому хочешь отправить сообщение", reply_markup=generate_keyboard_with_users(message.from_user.id))
    

@dp.message(SendAnonymousMessage.choice_user)
async def choice_user_anonymous(message: Message, state: FSMContext) -> None:
    try:
        username = message.text.split("@")[1][:-1]
    except:
        await message.answer("Что-то пошло не так, выберите снова", reply_markup=generate_keyboard_with_users(message.from_user.id))
    else:
        with db.session() as session:
            user = session.query(User).filter(User.username==username).first()
        await state.update_data(user=user)
        await state.set_state(SendAnonymousMessage.generate_message)
        await message.answer("Что хотите написать ему/ей?")

@dp.message(SendAnonymousMessage.generate_message)
async def generate_anonymous_message(message: Message, state: FSMContext) -> None:
    anon_text = "Вам сообщение от анонимного пользователя:\n" + message.text
    data = await state.get_data()
    user = data.get('user')
    await bot.send_message(user.telegram_id, anon_text)
    await message.answer('Сообщение отправлено!', reply_markup=generate_keyboard_with_menu())
    await state.clear()

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    db.check_exists_db()
    asyncio.run(main())