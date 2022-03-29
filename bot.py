# Наш главный файл бота через него мы запускаем его и отлавливаем нажатия кнопок
from keyboard import how_to_buy, how_to_sell, info_bot, channel_future
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboard import start_menu, shipping_menu, how_to_sell_menu, about_menu, alphabet_menu, \
    order_menu_buttons, add_offer_buttons, send_menu, send_menu_accept_inline, alphabet_menu_ru, get_back_buttons, \
     get_pref, get_values, add_skip_button, get_values_text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from db import get_box, get_engine_type
from fsms import DetailFSM, VinCodeFSM, FeedBackFSM, FeedBackAnswer, PhoneNumber
from aiogram.dispatcher import FSMContext
from db import get_mark_list, get_mark_markup, get_model_list, get_model_markup, get_generation_list, \
    get_generation_markup, get_steps, get_bodies, get_engine_volume, get_param, get_gen_year, get_all_cars, alphabet_buttons_ru_text

from config import TOKEN  # импортируем из config.py токен бота

bot = Bot(token=TOKEN)  # Передаем боту токен
dp = Dispatcher(bot, storage=MemoryStorage())

group_id = -1001729453823

answer = {}

admins = [1651350663]

tmp = {}
stack = {}

# Тут будут наши хендлеры
# *******************************************************************************************************


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):  # Отлавливаем команду /start
    if state:
        await state.finish()
    if message.from_user.username:
        await message.reply(f"Добро пожаловать, {message.from_user.username}  ! "
                            f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                            reply_markup=start_menu)
    else:
        await message.reply(f"Добро пожаловать, {message.from_user.first_name}  ! "
                            f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                            reply_markup=start_menu)


# Отлавливаем нажатие кнопки 'Как заказать'
@dp.callback_query_handler(text='help_shipping')
async def help_shipping(callback: types.CallbackQuery):
    await callback.message.answer(how_to_buy, reply_markup=shipping_menu)
    await callback.answer()


@dp.callback_query_handler(text="help_message")
async def feedback(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    await callback.message.answer('Введите ваше сообщение', reply_markup=menu)
    await FeedBackFSM.body.set()


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
    await callback.message.edit_text(channel_future, reply_markup=types.InlineKeyboardMarkup()
                                  .add(types.InlineKeyboardButton(text='🔙Назад', callback_data='help_about')))


# Отлавливаем нажатие кнопки 'Выход'
@dp.callback_query_handler(text='exit', state='*')
async def exit_handler(callback: types.CallbackQuery, state:FSMContext):
    if state:
        await state.finish()
        await callback.message.answer('Вы отменили ввод')
    await callback.message.edit_text('Добро пожаловать, car partsbot  ! Я @car_part_bot '
                                     '- удобный бот-по заказу и продаже автомабильных запчастей',
                                     reply_markup=start_menu)


@dp.callback_query_handler(text='buy_car_part')
async def get_alphabet_menu(callback: types.CallbackQuery):
    tmp[callback.message.chat.id] = {}

    await callback.message.answer('Выберите первую букву марки авто', reply_markup=alphabet_menu)
    await callback.answer()


@dp.callback_query_handler(text='buy_car_part_ru')
async def buy_part(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup()
    tmp[callback.message.chat.id]['letter'] = callback.data
    russian_cars = get_all_cars()
    L = sorted(list(frozenset([x.mark for x in russian_cars if x.mark[0] in alphabet_buttons_ru_text])))
    ru_cars = [types.InlineKeyboardButton(text=x, callback_data=f'mark_{x}') for x in L]
    menu.add(*ru_cars)
    get_back_buttons(markup=menu, back_command="buy_car_part")
    await callback.message.edit_text('Выберите марку авто', reply_markup=menu)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='letter_'))
async def auto_mark(callback: types.CallbackQuery):
    tmp[callback.message.chat.id] = {}
    tmp[callback.message.chat.id]['letter'] = callback.data
    menu = types.InlineKeyboardMarkup(row_width=2)
    letter = callback.data.split('_')[1]
    marks = get_mark_list(letter)
    keyboard = get_mark_markup(marks, letter)
    keyboard_buttons = [types.InlineKeyboardButton(text=x, callback_data=f'mark_{x}') for x in keyboard]
    menu.add(*keyboard_buttons)
    get_back_buttons(markup=menu, back_command="buy_car_part")
    await callback.message.edit_text(f'Укажите Марку авто', reply_markup=menu)


@dp.callback_query_handler(text='next')
async def next_mode(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup(row_width=2)
    mark = stack[callback.message.chat.id]['mark']
    models_list = get_model_list(mark)
    models = get_model_markup(models_list, mark)
    keyboard_buttons = [types.InlineKeyboardButton(text=x, callback_data=f'model_{x}') for x in models[97:]]
    menu.add(*keyboard_buttons)
    menu.row(types.InlineKeyboardButton(text='⏮', callback_data='prev'))
    get_back_buttons(markup=menu, back_command=tmp[callback.message.chat.id]['letter'])
    await callback.message.edit_text(f'Укажите модель авто', reply_markup=menu)


@dp.callback_query_handler(text='prev')
async def prev_model(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup(row_width=2)
    mark = stack[callback.message.chat.id]['mark']
    models_list = get_model_list(mark)
    models = get_model_markup(models_list, mark)
    keyboard_buttons = [types.InlineKeyboardButton(text=x, callback_data=f'model_{x}') for x in models[:97]]
    menu.add(*keyboard_buttons)
    if models[97:]:
        menu.row(types.InlineKeyboardButton(text='⏩', callback_data='next'))
    get_back_buttons(markup=menu, back_command=tmp[callback.message.chat.id]['letter'])
    await callback.message.edit_text(f'Укажите модель авто', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='mark_'))
async def auto_model(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup(row_width=2)
    mark = callback.data.split('_')[1]
    stack[callback.message.chat.id] = {}
    stack[callback.message.chat.id]['mark'] = mark
    tmp[callback.message.chat.id]['mark'] = callback.data
    models_list = get_model_list(mark)
    models = get_model_markup(models_list, mark)
    print(models[98:])
    keyboard_buttons = [types.InlineKeyboardButton(text=x, callback_data=f'model_{x}') for x in models[:97]]
    menu.add(*keyboard_buttons)
    if models[97:]:
        menu.row(types.InlineKeyboardButton(text='⏩', callback_data='next'))

    get_back_buttons(markup=menu, back_command=tmp[callback.message.chat.id]['letter'])
    await callback.message.edit_text(f'Укажите модель авто', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='model_'), state='*')
async def get_gen(callback: types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()
    menu = types.InlineKeyboardMarkup(row_width=1)
    model = callback.data.split('_')[1]
    tmp[callback.message.chat.id]['model'] = callback.data
    stack[callback.message.chat.id]['model'] = model
    generations = get_generation_list(model=model, mark=stack[callback.message.chat.id].get('mark'))
    keyboard_buttons = []
    for i in get_generation_markup(generations):
        text = i + ' ' + get_gen_year(mark=stack[callback.message.chat.id]['mark'], model=stack[callback.message.chat.id]['model'],
                     gen=i)
        keyboard_buttons.append(types.InlineKeyboardButton(text=text, callback_data=f'gen_{i}'))
    menu.add(*keyboard_buttons)
    if keyboard_buttons:
        if tmp[callback.message.chat.id].get('gen'):
            tmp[callback.message.chat.id].pop('gen')
        values = get_values(stack, callback)
        get_back_buttons(markup=menu, back_command=get_pref(tmp[callback.message.chat.id]))
        await callback.message.edit_text(f'Укажите поколение авто {values}', reply_markup=menu)
    else:
        if tmp[callback.message.chat.id].get('bodies'):
            tmp[callback.message.chat.id].pop('bodies')
        order_menu = types.InlineKeyboardMarkup(row_width=1)
        order_menu.add(*order_menu_buttons)
        values = get_values(stack, callback)
        get_back_buttons(markup=order_menu, back_command=get_pref(tmp[callback.message.chat.id]), exit_data='exit')
        await callback.message.edit_text(f'Вы выбрали {values}'
                                         f'Хотите указать дополнительные параметры: тип кузова, тип и объем '
                                         f'двигателя, тип коробки передач, VIN?', reply_markup=order_menu)


@dp.callback_query_handler(Text(startswith='gen_'))
async def get_params(callback: types.CallbackQuery):
    gen = callback.data.split('_')[1]
    tmp[callback.message.chat.id]['gen'] = callback.data
    stack[callback.message.chat.id]['gen'] = gen
    if tmp[callback.message.chat.id].get('order'):
        tmp[callback.message.chat.id].pop('order')
    order_menu = types.InlineKeyboardMarkup(row_width=1)
    order_menu.add(*order_menu_buttons)
    values = get_values(stack, callback)
    get_back_buttons(markup=order_menu, back_command=get_pref(tmp[callback.message.chat.id]))
    print(tmp)

    await callback.message.edit_text(f'Вы выбрали {values}'
                                     f'Хотите указать дополнительные параметры: тип кузова, тип и объем '
                                     f'двигателя, тип коробки передач, VIN?', reply_markup=order_menu)


@dp.callback_query_handler(Text(startswith='order'))
async def get_orders(callback: types.CallbackQuery):
    stack[callback.message.chat.id]['details'] = []
    order = callback.data.split('_')[1]
    tmp[callback.message.chat.id]['order'] = callback.data
    if order == 'add':
        if tmp[callback.message.chat.id].get('bodies'):
            tmp[callback.message.chat.id].pop('bodies')
        menu = types.InlineKeyboardMarkup(row_width=1)
        bodies = get_steps(stack[callback.message.chat.id].get('model'), stack[callback.message.chat.id].get('gen'))
        bodies_text = [types.InlineKeyboardButton(text=x, callback_data=f'body_{x}') for x in get_bodies(bodies) if x]
        menu.add(*bodies_text)
        values = get_values(stack, callback)
        add_skip_button(markup=menu, data='body_None')
        get_back_buttons(markup=menu, back_command=get_pref(tmp[callback.message.chat.id]))
        if tmp[callback.message.chat.id].get('order'):
            tmp[callback.message.chat.id].pop('order')
        await callback.message.edit_text(f'Вы выбрали {values} Выберите тип кузова', reply_markup=menu)
    elif order == 'skip':
        if tmp[callback.message.chat.id].get('bodies'):
            tmp[callback.message.chat.id].pop('bodies')
        stack[callback.message.chat.id]['details'] = []
        await DetailFSM.detail.set()
        await callback.message.answer('Введите название детали')


@dp.callback_query_handler(Text(startswith='body_'))
async def get_transmission(callback: types.CallbackQuery):
    if tmp[callback.message.chat.id].get('transmission'):
        tmp[callback.message.chat.id].pop('transmission')
    body = callback.data.split('_')[1]
    menu = types.InlineKeyboardMarkup(row_width=1)
    if body != 'None':
        stack[callback.message.chat.id]['body'] = body
    tmp[callback.message.chat.id]['bodies'] = callback.data
    transmissions = get_box(mark=stack[callback.message.chat.id].get('mark'),
                            model=stack[callback.message.chat.id].get('model'),
                            gen=stack[callback.message.chat.id].get('gen'),
                            body_type=stack[callback.message.chat.id].get('body'))
    transmissions_text = [types.InlineKeyboardButton(text=x, callback_data=f'transmission_{x}') for x in
                          transmissions if x]
    print(transmissions_text, transmissions)
    menu.add(*transmissions_text)
    add_skip_button(markup=menu, data='transmission_None')
    get_back_buttons(markup=menu, back_command=get_pref(tmp[callback.message.chat.id]))
    values = get_values(stack, callback)
    await callback.message.edit_text(f'Вы выбрали {values} Выберите тип коробки передач', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='transmission_'))
async def get_engine_types(callback: types.CallbackQuery):
    if tmp[callback.message.chat.id].get('engine_type'):
        tmp[callback.message.chat.id].pop('engine_type')
    transmission = callback.data.split('_')[1]
    menu = types.InlineKeyboardMarkup(row_width=1)
    if transmission != 'None':
        stack[callback.message.chat.id]['transmission'] = transmission
    tmp[callback.message.chat.id]['transmission'] = callback.data
    engine_type = get_engine_type(mark=stack[callback.message.chat.id].get('mark'),
                                  model=stack[callback.message.chat.id].get('model'),
                                  gen=stack[callback.message.chat.id].get('gen'),
                                  body_type=stack[callback.message.chat.id].get('body'),
                                  transmission=stack[callback.message.chat.id].get('transmission'))
    engine_type_text = [types.InlineKeyboardButton(text=x, callback_data=f'engine_{x}') for x in
                        engine_type if x]
    menu.add(*engine_type_text)
    add_skip_button(markup=menu, data='engine_None')
    get_back_buttons(markup=menu, back_command=get_pref(tmp[callback.message.chat.id]))
    values = get_values(stack, callback)
    await callback.message.edit_text(f'Вы выбрали {values} Выберите тип двигателя', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='engine_'), state='*')
async def set_engine_volume(callback: types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()
    if tmp[callback.message.chat.id].get('engine_volume'):
        tmp[callback.message.chat.id].pop('engine_volume')
    engine_type = callback.data.split('_')[1]
    menu = types.InlineKeyboardMarkup(row_width=1)
    if engine_type != 'None':
        stack[callback.message.chat.id]['engine_type'] = engine_type
    tmp[callback.message.chat.id]['engine_type'] = callback.data
    engine_volume = get_engine_volume(model=stack[callback.message.chat.id].get('model'),
                                      gen=stack[callback.message.chat.id].get('gen'),
                                      body_type=stack[callback.message.chat.id].get('body'),
                                      transmission=stack[callback.message.chat.id].get('transmission'),
                                      engine_type=stack[callback.message.chat.id].get('engine_type'))
    engine_volume_text = [types.InlineKeyboardButton(text=x, callback_data=f'volume_{x}') for x in
                          engine_volume if x]
    menu.add(*engine_volume_text)
    add_skip_button(markup=menu, data='volume_None')
    get_back_buttons(markup=menu, back_command=get_pref(tmp[callback.message.chat.id]))
    values = get_values(stack, callback)
    await callback.message.edit_text(f'Вы выбрали {values} Выберите объем двигателя', reply_markup=menu)


@dp.callback_query_handler(Text(startswith='volume_'))
async def set_vin_code(callback: types.CallbackQuery):
    if tmp[callback.message.chat.id].get('engine_volume'):
        tmp[callback].pop('engine_volume')
    mark_up = types.InlineKeyboardMarkup(row_width=1)
    mark_up.add(types.InlineKeyboardButton(text='Пропустить⏩', callback_data='None'))
    engine_volume = callback.data.split('_')[1]
    if engine_volume != "None":
        stack[callback.message.chat.id]['engine_volume'] = engine_volume
    tmp[callback.message.chat.id]['engine_volume'] = callback.data
    values = get_values(stack, callback)
    get_back_buttons(markup=mark_up, back_command=get_pref(tmp[callback.message.chat.id]))
    await VinCodeFSM.VIN.set()
    await callback.message.edit_text(f'Вы выбрали {values} Введите VIN код вашего авто', reply_markup=mark_up)


# *******************************************************************************************************


@dp.message_handler(state=DetailFSM.detail)
async def handle_menu(message: types.Message, state: FSMContext):
    add_offer_menu = types.InlineKeyboardMarkup(row_width=1)
    add_offer_menu.add(*add_offer_buttons)

    if len(message.text) > 5 and len(message.text) < 201:

        await DetailFSM.next()
        stack[message.chat.id]['details'].append(message.text)
        detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[message.chat.id]['details'], 1)]
        get_back_buttons(markup=add_offer_menu, back_command=get_pref(tmp[message.chat.id]), exit_data='pre_exit')
        char = get_param(tmp=stack, message=message)
        await message.answer(f'Ваш заказ на авто:\n'
                             f'{char}\n')
        await message.answer(f'Введите название нужной запчасти '
                             f'и при необходимости описание, '
                             f'особые пожелания по комплектации, '
                             f'цвету и т.д. (вводите название только '
                             f'одной запчасти, если необходимо '
                             f'несколько запчастей на это авто '
                             f'нажмите после ввода первой запчасти '
                             f'"Добавить еще запчасть на это авто ",'
                             f'если больше запчастей добавлять не '
                             f'нужно нажмите "оформить заказ")\n'
                             f'Вы уже добавили запчасти:\n'
                             f'\n{"".join(detail_list)}',
                             reply_markup=add_offer_menu)

    else:
        await message.answer('Название запчасти может быть от 5 до 200 символов введите более лаконичный заказ')


@dp.callback_query_handler(Text(startswith='offer_'))
async def order_manage(callback: types.CallbackQuery):
    if callback.data.split('_')[1] == 'make':
        value = get_values(stack, callback)
        detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[callback.message.chat.id]['details'], 1)]
        await callback.message.edit_text(f'Спасибо за Ваш заказ! '
                                      f'{value}\n'
                                      f'{" ".join(detail_list)} '
                                      f'чтобы получать предложения от '
                                      f'продавцов нажмите "поделиться '
                                      f'контактом"', reply_markup=send_menu)
    elif callback.data.split('_')[1] == 'add':
        await DetailFSM.detail.set()
        await callback.message.answer('Введите название детали')


@dp.message_handler(state=VinCodeFSM.VIN)
async def vin_handler(message: types.Message, state: FSMContext):
    await VinCodeFSM.next()
    if len(message.text) == 17 and message.text.isalnum():
        stack[message.chat.id]['vin'] = message.text
        await DetailFSM.next()
        await message.answer('Введите название детали')
    else:
        menu = types.InlineKeyboardMarkup()
        menu.add(types.InlineKeyboardButton(text='Отменить', callback_data='None'))
        await message.answer('это не похоже на VIN код попробуйте ввести еще раз', reply_markup=menu)
        await VinCodeFSM.next()


@dp.callback_query_handler(Text(startswith='send_'))
async def contact_handler(callback: types.CallbackQuery):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Предложить запчасть боту', callback_data='предложение'))
    if callback.data.split('_')[1] == 'no':
        await callback.message.edit_text(f'Вы уверены что хотите удалить свой заказ? '
                                      f'и вернуться в главное меню? '
                                      f'Можете отправить заказ "инкогнито "'
                                      f'если не хотите делится номером ', reply_markup=send_menu_accept_inline)
        await callback.answer()
    if callback.data.split('_')[1] == 'anon':
        await callback.message.answer('Вы отправили предложение анонимно в группу')
        values = get_param(tmp=stack, message=callback.message)
        detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[callback.message.chat.id]['details'], 1)]
        await bot.send_message(group_id, f'Заказ\n'
                                         f'{values}\n'
                                         f'Детали:\n{"".join(detail_list)}', reply_markup=menu)

        if callback.message.from_user.username:
                await callback.message.edit_text(f"Добро пожаловать, {callback.message.from_user.username}  ! "
                                             f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                                             reply_markup=start_menu)
        else:
                await callback.message.edit_text(f"Добро пожаловать, {callback.message.from_user.first_name}  ! "
                                             f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                                             reply_markup=start_menu)
    if callback.data.split('_')[1] == 'contact':
        get_contact = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton
                                                                          ('Отправить свой контакт ☎️',
                                                                           request_contact=True))
        get_contact.add(types.KeyboardButton('❌Отмена'))
        await callback.message.delete()
        await callback.message.answer('Отправьте ваш контакт', reply_markup=get_contact)
        await callback.answer()
        await PhoneNumber.number.set()


@dp.message_handler(state=PhoneNumber, content_types=['text'])
async def cancel(message: types.Message, state: FSMContext):
    if message.text =='❌Отмена':
        await state.finish()
        await message.answer('Вы отменили ввод номера', reply_markup=types.ReplyKeyboardRemove())
        value = get_values_text(stack, message)
        detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[message.chat.id]['details'], 1)]
        await message.answer(f'Спасибо за Ваш заказ! '
                                         f'{value}\n'
                                         f'{" ".join(detail_list)} '
                                         f'чтобы получать предложения от '
                                         f'продавцов нажмите "поделиться '
                                         f'контактом"', reply_markup=send_menu)


@dp.message_handler(state=PhoneNumber, content_types=['contact'])
async def get_number(message: types.Message, state: FSMContext):
    await message.answer('Вы отправили предложение в группу', reply_markup=types.ReplyKeyboardRemove())
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Предложить запчасть боту', callback_data='предложение'))
    if message.from_user.username:
        await message.reply(f"Добро пожаловать, {message.from_user.username}  ! "
                                     f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                                     reply_markup=start_menu)
    else:
        await message.reply(f"Добро пожаловать, {message.from_user.first_name}  ! "
                                     f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                                     reply_markup=start_menu)
    await state.finish()

    values = get_param(tmp=stack, message=message)
    detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[message.chat.id]['details'], 1)]
    await bot.send_message(group_id, f'Заказ\n'
                                     f'{values}\n'
                                     f'Детали:\n{"".join(detail_list)}', reply_markup=menu)


@dp.callback_query_handler(text='None', state='*')
async def skip_vin(callback: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:

        return

    await state.finish()
    await callback.answer()
    await DetailFSM.next()
    await callback.message.answer('Введите название детали')


@dp.callback_query_handler(text='state_exit', state='*')
async def back_down(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    await callback.answer()
    if callback.message.from_user.username:
        await callback.message.reply(f"Добро пожаловать, {callback.message.from_user.username}  ! "
                            f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                            reply_markup=start_menu)
    else:
        await callback.message.reply(f"Добро пожаловать, {callback.message.from_user.first_name}  ! "
                            f"Я @car_part_bot - удобный бот-по заказу и продаже автомабильных запчастей",
                            reply_markup=start_menu)


@dp.callback_query_handler(text='pre_exit')
async def pre_exit_check(callback: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Да', callback_data='exit'))
    markup.add(types.InlineKeyboardButton(text='Нет вернуться назад', callback_data='ord'))
    await callback.message.edit_text('Вы так старательно выбирали все данные, вы уверены что хотите удалить свой заказ полностью?', reply_markup=markup)


@dp.message_handler(state=FeedBackFSM)
async def get_feedback(message: types.Message):
    mark_up = types.InlineKeyboardMarkup()
    if len(message.text) < 10 or len(message.text) > 200:
        await message.answer('Ваще сообщение слишком длинное или слишком короткое')
    else:
        mark_up.add(types.InlineKeyboardButton(text='Ответить', callback_data=f'answ_{message.from_user.id}'))
        for i in admins:
            await bot.send_message(i, f'Сообщение от пользователя @{message.from_user.username}:\n{message.text}',
                                   reply_markup=mark_up)
        await message.answer('Ваш вопрос будет рассмотрен в ближайшее рабочее время')
        await FeedBackFSM.next()


@dp.callback_query_handler(Text(startswith='answ_'))
async def feed_back_answer(callback: types.CallbackQuery):
    answer['id'] = callback.data.split('_')[1]
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    await callback.message.answer('Введите свой ответ', reply_markup=menu)
    await FeedBackAnswer.body.set()


@dp.callback_query_handler(text='cancel', state='*')
async def skip_feedbacl(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    await callback.message.answer('Вы отменили ввод сообщение')
    await callback.answer()


@dp.message_handler(state=FeedBackAnswer)
async def send_answ_message(message: types.Message, state: FSMContext):
    await message.answer('Ваше сообщение отправлено')
    await bot.send_message(answer['id'], f'Сообщение от админа\n{message.text}')


@dp.callback_query_handler(text='ord')
async def ord_back(callback: types.CallbackQuery):
    add_offer_menu = types.InlineKeyboardMarkup(row_width=1)
    add_offer_menu.add(*add_offer_buttons)
    detail_list = [str(c) + ')' + x + '\n' for c, x in enumerate(stack[callback.message.chat.id]['details'], 1)]
    get_back_buttons(markup=add_offer_menu, back_command=get_pref(tmp[callback.message.chat.id]), exit_data='pre_exit')
    char = get_param(tmp=stack, message=callback.message)
    await callback.message.answer(f'Ваш заказ на авто:\n'
                                    f'{char}')
    await callback.message.answer(
                         f'Введите название нужной запчасти '
                         f'и при необходимости описание, '
                         f'особые пожелания по комплектации, '
                         f'цвету и т.д. (вводите название только '
                         f'одной запчасти, если необходимо '
                         f'несколько запчастей на это авто '
                         f'нажмите после ввода первой запчасти '
                         f'"Добавить еще запчасть на это авто", '
                         f'если больше запчастей добавлять не '
                         f'нужно нажмите "оформить заказ")\n '
                         f'Вы уже добавили запчасти:\n '
                         f'{"".join(detail_list)}',
                         reply_markup=add_offer_menu)

# Конец блока заказа
 #********************************************************************************************************************


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

