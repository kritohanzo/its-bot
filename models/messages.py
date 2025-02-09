from datetime import datetime
from enum import StrEnum

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy_utils import ChoiceType

from models.base import Base
from utils.mixins import ChoiceMixin


class MessagePrivacyTypeChoices(ChoiceMixin, StrEnum):
    ANONYMOUS = 'Анонимное'
    OPEN = 'Открытое'


class MessageContentTypeChoices(ChoiceMixin, StrEnum):
    TEXT = 'Текст'
    STICKER = 'Стикер'
    PHOTO = 'Фото'
    DOCUMENT = 'Документ'
    AUDIO = 'Аудио'
    VIDEO = 'Видео'
    VIDEO_NOTE = 'Кружок'
    VOICE = 'Голосовое'


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    recipient_id = Column(Integer)
    privacy_type = Column(ChoiceType(choices=MessagePrivacyTypeChoices.choices(), impl=String(length=9)))
    content_type = Column(ChoiceType(choices=MessageContentTypeChoices.choices(), impl=String(length=10)))
    created_at = Column(DateTime, default=datetime.now)
