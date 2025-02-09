from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class SendMessageState(StatesGroup):
    choice_privacy_type = State()
    choice_recipient = State()
    choice_content_type = State()
    choice_content = State()