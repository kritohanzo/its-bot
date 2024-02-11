from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class SendAnonymousMessage(StatesGroup):
    choice_user = State()
    generate_message = State()