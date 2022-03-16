''' Наш файл с набором всех кнопок и текстов которые мы будем импортировать в боте '''

from string import ascii_uppercase
from aiogram import types

# Тут будут наши кнопки
# *******************************************************************************************************
buttons_text = ['⚙️Как заказать', '💰Как продать', '🚘Добавить авто',
                '❌Удалить авто', '🗒Информация о боте', '📞Поддержка',
                '💰Заказать запчасть сейчас⚙️']

buttons_callbacks = ['help_shipping', 'help_sell', 'add_car',
                     'delete_car', 'help_about', 'help_message',
                     'buy_car_part']

start_back_button = types.InlineKeyboardButton(text="🔙Назад", callback_data='back')

alphabet_buttons = [types.InlineKeyboardButton(text=x, callback_data=f'letter_{x}') for x in ascii_uppercase]

inline_menu = [types.InlineKeyboardButton(text=buttons_text[x], callback_data=buttons_callbacks[x])
               for x in range(len(buttons_text))]

# *******************************************************************************************************


# Тут будет наше меню
# *******************************************************************************************************

start_menu = types.InlineKeyboardMarkup(row_width=2)
start_menu.add(*inline_menu)

shipping_menu = types.InlineKeyboardMarkup(row_width=1)
shipping_menu.add(inline_menu[-1], start_back_button)

# Меню которое появляется при нажатии кнопки 'Как заказать'
how_to_sell_menu = types.InlineKeyboardMarkup(row_width=1)
how_to_sell_menu.add(inline_menu[2], start_back_button)


# Меню которое появляется при нажатии кнопки 'Информация о боте'
about_menu = types.InlineKeyboardMarkup(row_width=1)
about_menu.add(inline_menu[2], inline_menu[3], inline_menu[-1],
               types.InlineKeyboardButton(text='📈Перспективы канала', callback_data='channel_future'),
               start_back_button)

# Меню
alphabet_menu = types.InlineKeyboardMarkup(row_width=5)
alphabet_menu.add(*alphabet_buttons)

# *******************************************************************************************************

# Тут будут переменные для чтения наших текстов


# *******************************************************************************************************


how_to_buy = open('text_messages/how_to_order.txt', 'r', encoding='utf8').read()

how_to_sell = open('text_messages/how_to_sell.txt', 'r', encoding='utf8').read()

info_bot = open('text_messages/about_bot.txt', 'r', encoding='utf8').read()

channel_future = open('text_messages/channel_future.txt', 'r', encoding='utf8').read()


# *******************************************************************************************************

