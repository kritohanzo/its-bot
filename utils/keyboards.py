from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from database.models import User
from database.utils import Database as db

def menu_keyboard():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text="Отправить анонимное сообщение")
    return menu_builder.as_markup()

def generate_users_keyboard(requester):
    users_builder = ReplyKeyboardBuilder()
    users = db.get(User)
    users = users.remove(requester)
    for user in users:
        users_builder.button(text=f'{user.full_name} (@{user.username})')
    return users_builder.as_markup()