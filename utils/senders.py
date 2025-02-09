from aiogram.types import Message as AiogramMessage
from aiogram import Bot
from models.messages import MessageContentTypeChoices, MessagePrivacyTypeChoices
from models.users import User

async def send_message_by_content_type(bot: Bot, recipient: User, message: AiogramMessage, content_type: MessageContentTypeChoices) -> None:
    match content_type:
        case MessageContentTypeChoices.TEXT:
            await bot.send_message(chat_id=recipient.telegram_id, text=message.text)
        case MessageContentTypeChoices.STICKER:
            await bot.send_sticker(chat_id=recipient.telegram_id, sticker=message.sticker.file_id)
        case MessageContentTypeChoices.PHOTO:
            photos = list(sorted(message.photo, key=lambda photo: photo.file_size))
            await bot.send_photo(chat_id=recipient.telegram_id, photo=photos[0].file_id)
        case MessageContentTypeChoices.DOCUMENT:
            await bot.send_document(chat_id=recipient.telegram_id, document=message.document.file_id)
        case MessageContentTypeChoices.AUDIO:
            await bot.send_audio(chat_id=recipient.telegram_id, audio=message.audio.file_id)
        case MessageContentTypeChoices.VIDEO:
            await bot.send_video(chat_id=recipient.telegram_id, video=message.video.file_id)
        case MessageContentTypeChoices.VIDEO_NOTE:
            await bot.send_video_note(chat_id=recipient.telegram_id, video_note=message.video_note.file_id)
        case MessageContentTypeChoices.VOICE:
            await bot.send_voice(chat_id=recipient.telegram_id, voice=message.voice.file_id)

async def send_notification_by_privacy_type(bot: Bot, sender: User, recipient: User, privacy_type: MessagePrivacyTypeChoices):
    match privacy_type:
        case MessagePrivacyTypeChoices.ANONYMOUS:
            await bot.send_message(chat_id=recipient.telegram_id, text="У вас новое анонимное сообщение:")
        case MessagePrivacyTypeChoices.OPEN:
            await bot.send_message(chat_id=recipient.telegram_id, text=f"У вас новое сообщение от @{sender.username}:")