from sqlalchemy import String, Column, Integer, DateTime
from models.base import Base
from sqlalchemy_utils import ChoiceType
from datetime import datetime
from enum import StrEnum
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
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    recipient_id = Column(Integer)
    privacy_type = Column(ChoiceType(choices=MessagePrivacyTypeChoices.choices(), impl=String(length=9)))
    content_type = Column(ChoiceType(choices=MessageContentTypeChoices.choices(), impl=String(length=10)))
    created_at = Column(DateTime, default=datetime.now)