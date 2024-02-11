from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from utils.models import User
from utils.db import Database as db

def generate_keyboard_with_menu():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text="Отправить анонимное сообщение")
    menu_builder.button(text="Генератор комплиментов")
    menu_builder.adjust(1)
    return menu_builder.as_markup(resize_keyboard=True)

def generate_keyboard_with_users(sender_telegram_id):
    with db.session() as session:
        users = session.query(User).filter(User.telegram_id != sender_telegram_id)
    users_builder = ReplyKeyboardBuilder()
    for user in users:
        users_builder.button(text=f'{user.full_name} (@{user.username})')
    users_builder.button(text='В главное меню')
    users_builder.adjust(1)
    return users_builder.as_markup()