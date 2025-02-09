from aiogram.fsm.state import State, StatesGroup


class SendMessageState(StatesGroup):
    choice_privacy_type = State()
    choice_recipient = State()
    choice_content_type = State()
    choice_content = State()
