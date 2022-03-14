'''Наш главный файл бота через него мы запускаем его и отлавливаем нажатия кнопок'''

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboard import start_menu
from client import FSMfeedback
from  keyboard import buttons
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN  # импортируем из config.py токен бота


bot = Bot(token=TOKEN)  # Передаем боту токен
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):  # Отлавливаем команду /start
    await message.reply(f"Добро пожаловать, {message.from_user.first_name}  ! "
                        f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                        reply_markup=start_menu)


# Отлавливаем нажатия наших кнопок
@dp.message_handler()
async def text_handler(message: types.Message):
    if message.text == buttons[0]:
        await message.answer('Тут будет справочная информация о том как заказать')
    if message.text == buttons[1]:
        await message.answer('Тут будет информация о том как продать')
    if message.text == buttons[2]:
        await message.answer('Тут мы будем добавлять наше авто')
    if message.text == buttons[3]:
        await message.answer('Тут мы будем удалять авто')
    if message.text == buttons[4]:
        await message.answer('Тут будет справочная информация о боте')
    if message.text == buttons[5]:
        await message.answer('Тут мы будем предлагать пользователю ввести его вопрос')
    if message.text == buttons[6]:
        await message.answer('Тут мы будет заказывать наши запчасти')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

