import asyncio
import os
import re

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message as AiogramMessage
from dotenv import load_dotenv

from models.messages import Message, MessageContentTypeChoices, MessagePrivacyTypeChoices
from models.users import User
from states.messages import GenerateComplimentState, SendMessageState
from utils.db import Database as db
from utils.finders import find_content_type_from_message
from utils.keyboards import back_to_menu_keyboard, menu_keyboard, privacy_types_keyboard, recipients_keyboard
from utils.mistral import MistralClient
from utils.senders import send_message_by_content_type, send_notification_by_privacy_type


load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(F.text.func(lambda text: text in ('/start', 'В главное меню')))
async def main_menu(message: AiogramMessage, state: FSMContext) -> None:
    with db.session() as session:
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

        if not user:
            user = User(
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_id=message.from_user.id,
            )

            session.add(instance=user)
            session.commit()

    await message.answer(text=f'Здравствуйте, @{message.from_user.username}', reply_markup=menu_keyboard())
    await state.clear()


@dp.message(F.text == 'Генератор комплиментов')
async def generate_compliment(message: AiogramMessage, state: FSMContext) -> None:
    await message.answer(text='Отправьте примерное описание генерируемого комплимента')
    await state.set_state(GenerateComplimentState.input_prompt)


@dp.message(GenerateComplimentState.input_prompt)
async def input_prompt(message: AiogramMessage, state: FSMContext) -> None:
    compliment = await MistralClient().get_compliment(prompt=message.text)
    await message.answer(text=str(compliment), reply_markup=menu_keyboard())
    await state.clear()


@dp.message(F.text == 'Отправить сообщение')
async def send_message(message: AiogramMessage, state: FSMContext) -> None:
    await message.answer(text='Выберите тип приватности отправляемого сообщения', reply_markup=privacy_types_keyboard())
    await state.set_state(SendMessageState.choice_privacy_type)


@dp.message(SendMessageState.choice_privacy_type, F.text.in_(MessagePrivacyTypeChoices.values()))
async def choice_privacy_type(message: AiogramMessage, state: FSMContext) -> None:
    await state.update_data(privacy_type=MessagePrivacyTypeChoices.from_value(value=message.text))
    await message.answer(
        text='Выберите получателя сообщения или введите его логин через @',
        reply_markup=recipients_keyboard(sender=message.from_user),
    )
    await state.set_state(SendMessageState.choice_recipient)


@dp.message(SendMessageState.choice_recipient)
async def choice_recipient(message: AiogramMessage, state: FSMContext) -> None:
    username_pattern = r'@(\w+)'
    match = re.findall(username_pattern, message.text)

    if not match:
        return await message.answer(
            text='Допущена ошибка в логине получателя, попробуйте снова',
            reply_markup=recipients_keyboard(sender=message.from_user),
        )

    with db.session() as session:
        recipient = session.query(User).filter(User.username == match[0]).first()

    if not recipient:
        return await message.answer(
            text='Получатель не зарегистрирован в боте, но вы можете выбрать другого',
            reply_markup=recipients_keyboard(sender=message.from_user),
        )

    await message.answer(
        text='Введите или прикрепите содержание отправляемого сообщения',
        reply_markup=back_to_menu_keyboard(),
    )

    await state.update_data(recipient=recipient)
    await state.set_state(SendMessageState.choice_content)


@dp.message(SendMessageState.choice_content)
async def choice_content(message: AiogramMessage, state: FSMContext) -> None:
    content_type: MessageContentTypeChoices = await find_content_type_from_message(message=message)

    if not content_type:
        return await message.answer(text='Ошибка при определении типа контента сообщения, попробуйте что-то другое')

    collected_data = await state.get_data()

    privacy_type: MessagePrivacyTypeChoices = collected_data.get('privacy_type')
    recipient: User = collected_data.get('recipient')

    try:
        await send_message_by_content_type(
            bot=bot,
            recipient=recipient,
            message=message,
            content_type=content_type,
        )

    except TelegramForbiddenError:
        await message.answer(
            text='Получатель запретил сообщения от бота, отправить ему сообщение не получится',
            reply_markup=menu_keyboard(),
        )
        return await state.clear()

    except TelegramBadRequest:
        return await message.answer(
            text='Получатель запретил получение данного типа контента, попробуйте отправить что-то другое'
        )

    await send_notification_by_privacy_type(
        bot=bot,
        sender=message.from_user,
        recipient=recipient,
        privacy_type=privacy_type,
    )

    with db.session() as session:
        sender = session.query(User).filter(User.telegram_id == message.from_user.id).first()

        new_message = Message(
            sender_id=sender.id,
            recipient_id=recipient.id,
            privacy_type=privacy_type.name,
            content_type=content_type.name,
        )

        session.add(instance=new_message)
        session.commit()

    await message.answer(text='Сообщение отправлено', reply_markup=menu_keyboard())
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    db.initialize_database()
    asyncio.run(main())
