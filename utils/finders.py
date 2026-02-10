from aiogram.types import Message as AiogramMessage

from models.messages import MessageContentTypeChoices


async def find_content_type_from_message(message: AiogramMessage) -> MessageContentTypeChoices | None:
    if message.text:
        return MessageContentTypeChoices.TEXT
    if message.sticker:
        return MessageContentTypeChoices.STICKER
    if message.photo:
        return MessageContentTypeChoices.PHOTO
    if message.document:
        return MessageContentTypeChoices.DOCUMENT
    if message.audio:
        return MessageContentTypeChoices.AUDIO
    if message.video:
        return MessageContentTypeChoices.VIDEO
    if message.video_note:
        return MessageContentTypeChoices.VIDEO_NOTE
    if message.voice:
        return MessageContentTypeChoices.VOICE
