from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Машина состояний для обратной связи


class FSMfeedback(StatesGroup):
    user = State()
    id = State()
    body = State()
