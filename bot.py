# Наш главный файл бота через него мы запускаем его и отлавливаем нажатия кнопок
from keyboard import how_to_buy, how_to_sell, info_bot, channel_future
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboard import start_menu, shipping_menu, how_to_sell_menu, about_menu, start_back_button, alphabet_menu
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN  # импортируем из config.py токен бота


bot = Bot(token=TOKEN)  # Передаем боту токен
dp = Dispatcher(bot, storage=MemoryStorage())

# Тут будут наши хендлеры
# *******************************************************************************************************


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):  # Отлавливаем команду /start
    await message.reply(f"Добро пожаловать, {message.from_user.first_name}  ! "
                        f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                        reply_markup=start_menu)


# Отлавливаем нажатие кнопки 'Как заказать'
@dp.callback_query_handler(text='help_shipping')
async def help_shipping(callback: types.CallbackQuery):
    await callback.message.answer(how_to_buy, reply_markup=shipping_menu)
    await callback.answer()


# Отлавливаем нажатие кнопки как продать
@dp.callback_query_handler(text='help_sell')
async def help_sell(callback: types.CallbackQuery):
    await callback.message.answer(how_to_sell, reply_markup=how_to_sell_menu)
    await callback.answer()


# Отлавливаем нажатие кнопки 'назад'
@dp.callback_query_handler(text='back')
async def back_button(callback: types.CallbackQuery):
    await callback.message.reply(f"Добро пожаловать, {callback.message.from_user.first_name}  ! "
                                 f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                                 reply_markup=start_menu)
    await callback.answer()


# Отлавливаем нажатие кнопки 'Информация о боте'
@dp.callback_query_handler(text='help_about')
async def about_bot(callback: types.CallbackQuery):
    await callback.message.answer(info_bot, reply_markup=about_menu)
    await callback.answer()


# Отлавливаем нажатие кнопки 'Перспективы канала'
@dp.callback_query_handler(text='channel_future')
async def bot_future(callback: types.CallbackQuery):
    await callback.message.answer(channel_future, reply_markup=types.InlineKeyboardMarkup().add(start_back_button))


# Отлавливаем кнопки 'заказать запчасть'
@dp.callback_query_handler(text='buy_car_part')
async def buy_part(callback: types.CallbackQuery):
    await callback.message.answer('Выберите первую букву марки авто', reply_markup=alphabet_menu)
    await callback.answer()


# Отлавливаем нажатие кнопки 'Выход'
@dp.callback_query_handler(text='exit')
async def exit_handler(callback: types.CallbackQuery):
    await callback.message.edit_text('Добро пожаловать, car partsbot  ! Я @car_part_bot '
                                     '- удобный бот-по заказу и продаже автомабильных запчастей',
                                     reply_markup=start_menu)


# *******************************************************************************************************


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

