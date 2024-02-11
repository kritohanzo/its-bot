from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from database.models import User
from database.utils import Database as db

def menu_keyboard():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text="Отправить анонимное сообщение хуесосу")
    return menu_builder.as_markup(resize_keyboard=True)

def generate_users_keyboard(requester):
    with db.session() as session:
        users = session.query(User).filter(User.telegram_id != requester)
    users_builder = ReplyKeyboardBuilder()
    users_builder.adjust(3, 2)
    for user in users:
        users_builder.button(text=f'{user.full_name} (@{user.username})')
    return users_builder.as_markup()