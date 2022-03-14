''' Наш файл с набором всех кнопок которые мы будем импортировать в боте '''

from aiogram import types

# Меню
buttons = ['Как заказать', 'Как продать', 'Добавить авто',
           'Удалить авто', 'Информация о боте', 'Поддержка',
           'Заказать запчасть сейчас']

start_menu = types.ReplyKeyboardMarkup()
# проходимся циклом по кнопкам и ставим каждые 2 кнопки в 1 ряд
[start_menu.row(button, buttons[i-1]) for i, button in enumerate(buttons[:-1]) if (i+1) % 2 == 0 and i + 1 != 0]

start_menu.row(types.KeyboardButton(buttons[-1])) # Заказать запчасть сейчас
