from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from os.path import join, dirname
from database.models import User
from database.utils import Database as db
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
from utils.keyboards import menu_keyboard, generate_users_keyboard


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

dp = Dispatcher()

class Form(StatesGroup):
    name = State()

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    user = db.get(User, telegram_id=message.from_user.id, first=True)
    if user:
        await message.answer(f"Снова привет, {message.from_user.first_name} 🙂", reply_markup=menu_keyboard())
    else:
        new_user = User(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
        db.create(new_user)
        await message.answer(f"Привет, {message.from_user.first_name}, вижу тебя впервые, добро пожаловать 🙂", reply_markup=menu_keyboard())


@dp.message(F.text=="Отправить анонимное сообщение")
async def send_anon_message(message: Message, state: FSMContext) -> None:
    user = db.get(User, telegram_id=message.from_user.id, first=True)
    await message.answer(f"Выбери, кому хочешь отправить сообщение", reply_markup=generate_users_keyboard(user))

@dp.message(F.text=="Назад")
async def not_found(message: Message, state: FSMContext) -> None:
    await state.clear()
    await start_command(message, state)

async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    db.check_exists_db()
    asyncio.run(main())