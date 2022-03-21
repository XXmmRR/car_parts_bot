# Наш главный файл бота через него мы запускаем его и отлавливаем нажатия кнопок
from keyboard import how_to_buy, how_to_sell, info_bot, channel_future
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboard import start_menu, shipping_menu, how_to_sell_menu, about_menu, start_back_button, alphabet_menu, \
    order_menu, add_offer_menu, send_menu, send_menu_accept_inline
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from db import BaseCars, Session
from fsms import DetailFSM, VinCodeFSM
from aiogram.dispatcher import FSMContext

from config import TOKEN  # импортируем из config.py токен бота

bot = Bot(token=TOKEN)  # Передаем боту токен
dp = Dispatcher(bot, storage=MemoryStorage())

group_id = -1001729453823

tmp = {}

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


# Блок заказа запчастей
# *******************************************************************************************************


# Отлавливаем кнопки 'заказать запчасть'
@dp.callback_query_handler(text='buy_car_part')
async def buy_part(callback: types.CallbackQuery):
    await callback.message.answer('Выберите первую букву марки авто', reply_markup=alphabet_menu)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='letter_'))
async def set_letter(callback: types.CallbackQuery):
    order = types.InlineKeyboardMarkup(row_width=2)
    user_key_board = []
    letter = callback.data.split('_')[1]
    session = Session()
    mark = session.query(BaseCars).filter(BaseCars.mark.like(f'{letter}%')).all()
    session.close()
    [user_key_board.append(x.mark) for x in mark]
    menu = [types.InlineKeyboardButton(text=x, callback_data=f'mark_{x}') for x in list(set(user_key_board))]
    order.add(*menu)
    order.row(start_back_button, types.InlineKeyboardButton(text="❌Выход", callback_data='exit'))
    await callback.message.edit_text(f'Укажите марку авто ', reply_markup=order)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='mark_'))
async def set_mark(callback: types.CallbackQuery):
    tmp[callback.message.chat.id] = {}
    mark_name = callback.data.split('_')[1]
    order = types.InlineKeyboardMarkup(row_width=2)
    user_key_board = []
    session = Session()
    model = session.query(BaseCars).filter(BaseCars.mark.like(f'{mark_name}%')).all()
    session.close()
    [user_key_board.append(x.model) for x in model]
    menu = [types.InlineKeyboardButton(text=x, callback_data=f'model_{x}') for x in sorted(list(set(user_key_board)))
            if x]
    order.add(*menu)
    order.row(start_back_button, types.InlineKeyboardButton(text="❌Выход", callback_data='exit'))
    tmp[callback.message.chat.id]['mark_name'] = mark_name
    await callback.message.edit_text(f'Укажите модель авто {mark_name}', reply_markup=order)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='model_'))
async def set_model(callback: types.CallbackQuery):
    order = types.InlineKeyboardMarkup(row_width=2)
    user_key_board = []
    session = Session()
    model_name = callback.data.split('_')[1]
    generation = session.query(BaseCars).filter(BaseCars.model.like(f'{model_name}')).all()
    session.close()
    [user_key_board.append(x.generation) for x in generation if x.generation]
    if user_key_board:  # Проверяем есть ли поколение
        menu = [types.InlineKeyboardButton(text=x, callback_data=f'gen_{x}') for x in sorted(list(set(user_key_board)))]
        order.add(*menu)
        tmp[callback.message.chat.id]['model'] = model_name
        order.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
        await callback.message.edit_text(f'Укажите поколение авто {model_name}', reply_markup=order)
    else:
        tmp[callback.message.chat.id]['model'] = model_name
        values = [str(x)+' ' for x in tmp[callback.message.chat.id].values( ) if x]
        await callback.message.edit_text(f'Вы выбрали  {"".join(values)}'
                                         f'Хотите указать дополнительные параметры: тип кузова, тип и объем'
                                         f'двигателя, тип коробки передач, VIN?', reply_markup=order_menu)


@dp.callback_query_handler(Text(startswith='gen_'))
async def set_get(callback: types.CallbackQuery):
    gen_name = callback.data.split('_')[1]
    tmp[callback.message.chat.id]['gen_name'] = gen_name
    values = [str(x) + ' ' for x in tmp[callback.message.chat.id].values() if x]
    await callback.message.edit_text(f'Вы выбрали {"".join(values)}'
                                     f'Хотите указать дополнительные параметры: тип кузова, тип и объем'
                                     f'двигателя, тип коробки передач, VIN?', reply_markup=order_menu)


@dp.callback_query_handler(Text(startswith='order_'))
async def order(callback: types.CallbackQuery):
    tmp[callback.message.chat.id]['details'] = []
    if callback.data.split('_')[1] == 'skip':

        await DetailFSM.next()

        await callback.message.answer('Введите название детали')
        await callback.answer()
    elif callback.data.split('_')[1] == 'add':
        mark_up = types.InlineKeyboardMarkup(row_width=1)
        user_key_board = []
        session = Session()
        body_types = session.query(BaseCars).filter(BaseCars.model.like
                                                    (f'{tmp[callback.message.chat.id]["model"]}')).all()
        [user_key_board.append(x.body_type) for x in body_types]
        menu = [types.InlineKeyboardButton(text=x, callback_data=f'body_{x}') for x in
                sorted(list(set(user_key_board)))]
        mark_up.add(*menu)
        mark_up.add(types.InlineKeyboardButton(text='Пропустить', callback_data='body_None'))
        mark_up.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
        values = [str(x)+' ' for x in tmp[callback.message.chat.id].values() if x]
        await callback.message.edit_text(f'Вы выбрали  {"".join(values)}'
                                         f' Выберите тип кузова', reply_markup=mark_up)


# Отлов типа кузова
@dp.callback_query_handler(Text(startswith='body_'))
async def set_transmission(callback: types.CallbackQuery):
    mark_up = types.InlineKeyboardMarkup(row_width=1)
    user_key_board = []
    session = Session()
    body_types = session.query(BaseCars).filter(BaseCars.model.like
                                                (f'{tmp[callback.message.chat.id]["model"]}')).all()
    [user_key_board.append(x.transmission) for x in body_types]
    menu = [types.InlineKeyboardButton(text=x, callback_data=f'transmission_{x}') for x in
            sorted(list(set(user_key_board)))]
    mark_up.add(*menu)
    mark_up.add(types.InlineKeyboardButton(text='Пропустить', callback_data='transmission_None'))
    mark_up.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
    if callback.data.split('_')[1] == 'None':
        tmp[callback.message.chat.id]['body_type'] = None
        await callback.message.edit_text('Выберите коробку передач', reply_markup=mark_up)
        await callback.message.answer('Пропустить')
        await callback.answer()
    else:
        tmp[callback.message.chat.id]['body_type'] = callback.data.split('_')[1]
        await callback.message.edit_text('Выберите коробку передач', reply_markup=mark_up)
        await callback.answer()


# Выбор трансмиссии
@dp.callback_query_handler(Text(startswith='transmission_'))
async def set_engine_type(callback: types.CallbackQuery):
    mark_up = types.InlineKeyboardMarkup(row_width=1)
    user_key_board = []
    session = Session()
    body_types = session.query(BaseCars).filter(BaseCars.model.like
                                                (f'{tmp[callback.message.chat.id]["model"]}')).all()
    [user_key_board.append(x.engine_type) for x in body_types]
    menu = [types.InlineKeyboardButton(text=x, callback_data=f'fuel_{x}') for x in
            sorted(list(set(user_key_board)))]
    mark_up.add(*menu)
    mark_up.add(types.InlineKeyboardButton(text='Пропустить', callback_data='fuel_None'))
    mark_up.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
    if callback.data.split('_')[1] == 'None':
        await callback.message.edit_text('Выберите тип двигателя', reply_markup=mark_up)
        tmp[callback.message.chat.id]['transmission'] = None
        await callback.message.answer('Пропустить')
    else:
        tmp[callback.message.chat.id]['transmission'] = callback.data.split('_')[1]
        await callback.message.edit_text("Выберите тип двигателя", reply_markup=mark_up)


@dp.callback_query_handler(Text(startswith='fuel'))
async def engine_contain(callback: types.CallbackQuery):
    user_key_board = []
    session = Session()
    if callback.data.split('_')[1] == 'None':
        tmp[callback.message.chat.id]['volume'] = None
        await callback.message.answer('Пропустить')
    else:
        tmp[callback.message.chat.id]['volume'] = callback.data.split('_')[1]
        fuel_contain = session.query(BaseCars).filter(BaseCars.model.like
                                                      (f'{tmp[callback.message.chat.id]["model"]}')).all()
        [user_key_board.append(x.volume) for x in fuel_contain if x]
        mark_up = types.InlineKeyboardMarkup(row_width=1)
        menu = [types.InlineKeyboardButton(text=x, callback_data=f'contain_{x}') for x in
                sorted(list(set(user_key_board))) if x]
        mark_up.add(*menu)
        mark_up.add(types.InlineKeyboardButton(text='Пропустить', callback_data='contain_None'))
        mark_up.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
        await callback.message.edit_text('Выберите обьем двигателя', reply_markup=mark_up)


# Выбор топлива
@dp.callback_query_handler(Text(startswith='contain'))
async def set_engine_value(callback: types.CallbackQuery):
    mark_up = types.InlineKeyboardMarkup(row_width=1)
    mark_up.add(types.InlineKeyboardButton(text='Пропустить', callback_data='None'))
    mark_up.row(types.InlineKeyboardButton(text="❌Выход", callback_data='exit'), start_back_button)
    if callback.data.split('_')[1] == 'None':
        await VinCodeFSM.VIN.set()
        tmp[callback.message.chat.id]['contain'] = None
        await callback.message.answer('Введите VIN код вашего авто', reply_markup=mark_up)
    else:
        tmp[callback.message.chat.id]['contain'] = callback.data.split('_')[1]
        values = [str(x)+' ' for x in tmp[callback.message.chat.id].values() if x]
        await VinCodeFSM.VIN.set()
        await callback.message.edit_text(f'Вы выбрали {"".join(values)}'
                                         f'Введите VIN код вашего авто', reply_markup=mark_up)


@dp.callback_query_handler(Text(startswith='offer_'))
async def order_manage(callback: types.CallbackQuery):
    if callback.data.split('_')[1] == 'make':
        values = [str(x)+' ' for x in tmp[callback.message.chat.id].values() if not isinstance(x, list)]
        detail_list = [x+'\n' for x in tmp[callback.message.chat.id]['details']]
        await callback.message.edit_text(f'Спасибо за Ваш заказ! '
                                      f'{" ".join(values)}'
                                      f'{" ".join(detail_list)}'
                                      f'чтобы получать предложения от'
                                      f'продавцов нажмите "поделиться '
                                      f'контактом"', reply_markup=send_menu)
    elif callback.data.split('_')[1] == 'add':
        await DetailFSM.detail.set()
        await callback.message.answer('Введите название детали')


@dp.message_handler(state=VinCodeFSM.VIN)
async def vin_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vin'] = message.text
        await VinCodeFSM.next()
    if len(message.text) == 17 and message.text.isalnum():
        tmp[message.chat.id]['vin'] = message.text
        await DetailFSM.next()
        await message.answer('Введите название детали')
    else:
        await message.answer('Vin код должен быть длинной 17 символов введите его заново')
        tmp[message.chat.id]['vin'] = message.text

        async with state.proxy() as data:
            data['vin'] = message.text
            await VinCodeFSM.next()


@dp.message_handler(state=DetailFSM.detail)
async def handle_menu(message: types.Message, state: FSMContext):
    if len(message.text) > 5:

        async with state.proxy() as data:
            data['detail'] = message.text
            await DetailFSM.next()
            tmp[message.chat.id]['details'].append(message.text)
            detail_list = [x + '\n' for x in tmp[message.chat.id]['details']]

        await message.answer(f'Введите название нужной запчасти'
                             f'и при необходимости описание,'
                             f'особые пожелания по комплектации,'
                             f'цвету и т.д. (вводите название только'
                             f'одной запчасти, если необходимо'
                             f'несколько запчастей на это авто'
                             f'нажмите после ввода первой запчасти'
                             f'"Добавить еще запчасть на это авто",'
                             f'если больше запчастей добавлять не'
                             f'нужно нажмите "оформить заказ")\n'
                             f'{"".join(detail_list)}',
                             reply_markup=add_offer_menu)

    else:
        await message.answer('Название детали слишком короткое')


@dp.callback_query_handler(text='None', state='*')
async def skip_vin(callback: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:

        return

    await state.finish()
    await callback.answer()
    await DetailFSM.next()

    await callback.message.answer('Введите название детали')


@dp.callback_query_handler(Text(startswith='send_'))
async def contact_handler(callback: types.CallbackQuery):
    detail_list = [x + '\n' for x in tmp[callback.message.chat.id]['details']]
    parameters = ''
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Предложить запчасть боту', callback_data='предложение'))
    for key, value in tmp[callback.message.chat.id].items():
        if key != 'details':
            if value:
                parameters = parameters + key + " : " + value + '\n'
    parameters = parameters.replace('mark_name', 'Марка').replace('model', 'Модель').replace('transmission', 'КПП') \
        .replace('body_type', 'Кузов').replace('volume', 'Тип двигателя').replace('vin', 'VIN') \
        .replace('gen_name', 'Поколение').replace('contain', 'Обьем двигателя')
    if callback.data.split('_')[1] == 'no':
        await callback.message.edit_text(f'Вы уверены что хотите удалить свой заказ?'
                                      f'и вернуться в главное меню?'
                                      f'Можете отправить заказ "инкогнито"'
                                      f'если не хотите делится номером', reply_markup=send_menu_accept_inline)
        await callback.answer()
    if callback.data.split('_')[1] == 'anon':
        await callback.message.answer('Вы отправили предложение анонимно в группу')
        await bot.send_message(group_id, f'Заказ\n'
                                         f'{parameters}\n'
                                         f'Детали:\n{"".join(detail_list)}', reply_markup=menu)
    if callback.data.split('_')[1] == 'contact':

        await bot.send_message(group_id, f'Заказ\n'
                                         f'{parameters}\n'
                                         f'Детали:\n{"".join(detail_list)}', reply_markup=menu)
        await callback.message.answer('Вы отправили предложение в группу')

# Конец блока запчасти
# *******************************************************************************************************


# Отлавливаем нажатие кнопки 'Выход'
@dp.callback_query_handler(text='exit')
async def exit_handler(callback: types.CallbackQuery, ):
    await callback.message.edit_text('Добро пожаловать, car partsbot  ! Я @car_part_bot '
                                     '- удобный бот-по заказу и продаже автомабильных запчастей',
                                     reply_markup=start_menu)


# *******************************************************************************************************


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

