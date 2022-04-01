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
a = ord('а')
alphabet_buttons_ru_text = ''.join([chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)])\
    .replace('ь', '').replace('ы', '').replace('ъ', '').upper()

alphabet_buttons_ru = [types.InlineKeyboardButton(text=x, callback_data=f'letter_{x}') for x in
                       alphabet_buttons_ru_text]


inline_menu = [types.InlineKeyboardButton(text=buttons_text[x], callback_data=buttons_callbacks[x])
               for x in range(len(buttons_text))]


order_menu_text = ['🔧Указать доп параметры', 'Пропустить доп параметры⏩']
order_menu_callbacks = ['order_add', 'order_skip']
order_menu_buttons = [types.InlineKeyboardButton(text=order_menu_text[x], callback_data=order_menu_callbacks[x])
                      for x in range(len(order_menu_text))]

add_offer_text = ['💰Оформить заказ ', '➕Добавить еще запчасть на это авто']
add_offer_callbacks = ['offer_make', 'offer_add']
add_offer_buttons = [types.InlineKeyboardButton(text=add_offer_text[x], callback_data=add_offer_callbacks[x])
                     for x in range(len(order_menu_text))]

# Блок отправления контакта продавцу запчасти

send_contact_block_text = ['✅Поделится контактом', '➕Добавить еще запчасть на авто', '❌Не отправлять предложение']
send_contact_block_callbacks = ['send_contact', 'offer_add', 'send_no']
send_contact_block_menu = [types.InlineKeyboardButton(text=send_contact_block_text[x],
                          callback_data=send_contact_block_callbacks[x])
                          for x in range(len(send_contact_block_text))]

send_contact_block_text_accept = ['❌Да', '⏩Нет, вернуться к отправке', '📵Отправить заказ не делясь контактом']
send_contact_block_callbacks_accept = ['exit', 'offer_make', 'send_anon']
send_contact_block_accept_menu = [types.InlineKeyboardButton(text=send_contact_block_text_accept[x],
                          callback_data=send_contact_block_callbacks_accept[x])
                          for x in range(len(send_contact_block_text_accept))]

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
alphabet_menu.add(*alphabet_buttons[:-6])
alphabet_menu.row(*alphabet_buttons[-6:])
alphabet_menu.add(types.InlineKeyboardButton(text="Авто с русскими названиями", callback_data='buy_car_part_ru'))
alphabet_menu.row(start_back_button, types.InlineKeyboardButton(text='❌Выход', callback_data='exit'))


alphabet_menu_ru = types.InlineKeyboardMarkup(row_width=5)
alphabet_menu_ru.add(*alphabet_buttons_ru)
alphabet_menu_ru.add(types.InlineKeyboardButton(text="Авто с английскими названиями", callback_data='buy_car_part'))
alphabet_menu_ru.row(start_back_button, types.InlineKeyboardButton(text='❌Выход', callback_data='exit'))

order_menu = types.InlineKeyboardMarkup(row_width=1)
order_menu.add(*order_menu_buttons)


add_offer_menu = types.InlineKeyboardMarkup(row_width=1)
add_offer_menu.add(*add_offer_buttons)
add_offer_menu.row(start_back_button, types.InlineKeyboardButton(text="❌Выход", callback_data='exit'))


send_menu = types.InlineKeyboardMarkup(row_width=1)
send_menu.add(*send_contact_block_menu)

send_menu_accept_inline = types.InlineKeyboardMarkup(row_width=1)
send_menu_accept_inline.add(*send_contact_block_accept_menu)

# *******************************************************************************************************

# Тут будут переменные для чтения наших текстов


# *******************************************************************************************************


how_to_buy = open('text_messages/how_to_order.txt', 'r', encoding='utf8').read()

how_to_sell = open('text_messages/how_to_sell.txt', 'r', encoding='utf8').read()

info_bot = open('text_messages/about_bot.txt', 'r', encoding='utf8').read()

channel_future = open('text_messages/channel_future.txt', 'r', encoding='utf8').read()


# *******************************************************************************************************

#

def get_pref(tmp):
    return tmp[list(tmp.keys())[-2]]


def get_back_buttons(markup, back_command, exit_data='exit', exit_text ='❌Выход', back_text='🔙Назад'):
    markup.row(types.InlineKeyboardButton(text=back_text, callback_data=f'{back_command}'),
              types.InlineKeyboardButton(text=exit_text, callback_data=exit_data))


def get_values_text(tmp, message):
    return ''.join([str(x) + ' ' for x in tmp[message.chat.id].values() if x and not isinstance(x, list)])


def get_values(tmp, sec_dict):
    return ''.join([str(x) + ' ' for x in tmp[sec_dict.message.chat.id].values() if x and not isinstance(x, list)])


def add_skip_button(markup, data):
    markup.add(types.InlineKeyboardButton(text='Пропустить⏩', callback_data=data))


def gen_year(values, gen, year):
    if gen:
        gen_pos = values.find(gen[-1]) + len(gen)
        return values[:gen_pos] + ' ' + year + values[gen_pos:]
    else:
        return values

