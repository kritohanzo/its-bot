from aiogram.types import User as AiogramUser
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models.messages import MessageContentTypeChoices, MessagePrivacyTypeChoices
from models.users import User
from utils.db import Database as db


def back_to_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text='В главное меню')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Отправить сообщение')
    builder.button(text='Генератор комплиментов')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def privacy_types_keyboard():
    builder = ReplyKeyboardBuilder()

    for _, value in MessagePrivacyTypeChoices.choices():
        builder.button(text=value)

    builder.button(text='В главное меню')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def recipients_keyboard(sender: AiogramUser):
    with db.session() as session:
        users = session.query(User).filter(User.telegram_id != sender.id)

    builder = ReplyKeyboardBuilder()

    for user in users:
        builder.button(text=f'{user.full_name} (@{user.username})')

    builder.button(text='В главное меню')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def content_types_keyboard():
    builder = ReplyKeyboardBuilder()

    for _, value in MessageContentTypeChoices.choices():
        builder.button(text=value)

    builder.button(text='В главное меню')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
