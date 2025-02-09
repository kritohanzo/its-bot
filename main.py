from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from models.users import User
from models.compliments import Compliment
from models.messages import Message, MessagePrivacyTypeChoices, MessageContentTypeChoices
from utils.db import Database as db
from aiogram.filters import CommandStart
from aiogram.types import Message as AiogramMessage, User as AiogramUser
import os
import asyncio
from aiogram.enums import ParseMode
from utils.keyboards import menu_keyboard, recipients_keyboard, back_to_menu_keyboard, privacy_types_keyboard, content_types_keyboard
from states.messages import SendMessageState
from sqlalchemy import func
from utils.senders import send_message_by_content_type, send_notification_by_privacy_type
import re


load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(F.text.func(lambda text: text in ('/start', 'В главное меню')))
async def main_menu(message: AiogramMessage, state: FSMContext) -> None:
    with db.session() as session:
        user = session.query(User).filter(
            User.telegram_id==message.from_user.id,
        ).first()

        if not user:
            user = User(
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_id=message.from_user.id
            )

            session.add(instance=user)
            session.commit()

    await message.answer(text=f"Здравствуйте, @{message.from_user.username}", reply_markup=menu_keyboard())
    await state.clear()


@dp.message(F.text=="Генератор комплиментов")
async def generate_compliment(message: AiogramMessage, state: FSMContext) -> None:
    with db.session() as session:
        compliment = session.query(Compliment).order_by(func.random()).first()

    await message.answer(text=compliment.text, reply_markup=menu_keyboard())


@dp.message(F.text=="Отправить сообщение")
async def send_message(message: AiogramMessage, state: FSMContext) -> None:
    await message.answer(text="Выберите тип приватности отправляемого сообщения", reply_markup=privacy_types_keyboard())
    await state.set_state(SendMessageState.choice_privacy_type)


@dp.message(SendMessageState.choice_privacy_type, F.text.in_(MessagePrivacyTypeChoices.values()))
async def choice_privacy_type(message: AiogramMessage, state: FSMContext) -> None:
    await state.update_data(privacy_type=MessagePrivacyTypeChoices.from_value(value=message.text))
    await message.answer(text="Выберите получателя сообщения или введите его логин через @", reply_markup=recipients_keyboard(sender=message.from_user))
    await state.set_state(SendMessageState.choice_recipient)


@dp.message(SendMessageState.choice_recipient)
async def choice_recipient(message: AiogramMessage, state: FSMContext) -> None:
    username_pattern = r'@(\w+)'
    match = re.findall(username_pattern, message.text)

    if not match:
        return await message.answer(text="Допущена ошибка в логине получателя, попробуйте снова", reply_markup=recipients_keyboard(sender=message.from_user))

    with db.session() as session:
        recipient = session.query(User).filter(User.username==match[0]).first()

    if not recipient:
        return await message.answer(text="Получатель не зарегистрирован в боте, но вы можете выбрать другого", reply_markup=recipients_keyboard(sender=message.from_user))

    await message.answer(text="Выберите тип контента отправляемого сообщения", reply_markup=content_types_keyboard())
    await state.update_data(recipient=recipient)
    await state.set_state(SendMessageState.choice_content_type)


@dp.message(SendMessageState.choice_content_type, F.text.in_(MessageContentTypeChoices.values()))
async def choice_content_type(message: AiogramMessage, state: FSMContext) -> None:
    await message.answer(text="Введите или прикрепите содержание отправляемого сообщения", reply_markup=back_to_menu_keyboard())
    await state.update_data(content_type=MessageContentTypeChoices.from_value(value=message.text))
    await state.set_state(SendMessageState.choice_content)


@dp.message(SendMessageState.choice_content)
async def choice_content(message: AiogramMessage, state: FSMContext) -> None:
    collected_data = await state.get_data()
    
    content_type: MessageContentTypeChoices = collected_data.get('content_type')
    privacy_type: MessagePrivacyTypeChoices = collected_data.get('privacy_type')
    recipient: User = collected_data.get('recipient')

    if not getattr(message, collected_data.get('content_type').name.lower()):
        return await message.answer(text='Выбранный тип контента не совпадает с отправляемым', reply_markup=back_to_menu_keyboard())

    await send_notification_by_privacy_type(bot=bot, sender=message.from_user, recipient=recipient, privacy_type=privacy_type)
    await send_message_by_content_type(bot=bot, recipient=recipient, message=message, content_type=content_type)
    
    with db.session() as session:
        sender: User = session.query(User).filter(User.telegram_id==message.from_user.id).first()
        
        new_message = Message(
            sender_id=sender.id,
            recipient_id=recipient.id,
            privacy_type=privacy_type.name,
            content_type=content_type.name,
        )

        session.add(instance=new_message)
        session.commit()

    await message.answer(text="Сообщение отправлено", reply_markup=menu_keyboard())
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    db.initialize_database()
    db.initialize_compliments()
    asyncio.run(main())