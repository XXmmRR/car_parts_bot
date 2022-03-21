from aiogram.dispatcher.filters.state import StatesGroup, State


class WelcomeDetailFSM(StatesGroup):
    detail = State()


class DetailFSM(StatesGroup):
    detail = State()


class VinCodeFSM(StatesGroup):
    VIN = State()
