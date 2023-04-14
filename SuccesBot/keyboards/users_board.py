from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


first = ReplyKeyboardMarkup(resize_keyboard=True)
getPers = KeyboardButton('Получить персонажа👤')
first.row(getPers)

second = ReplyKeyboardMarkup(resize_keyboard=True)
getPersInfo = KeyboardButton('Мой персонаж👤')
second.row(getPersInfo)


Go_in_event = InlineKeyboardMarkup(row_width=1)
Accept_event = InlineKeyboardButton(callback_data='go_in_event', text="✅")
NotAccept_event = InlineKeyboardButton(callback_data='not_in_event', text="❌")
Go_in_event.add(Accept_event)

IsAccept = InlineKeyboardMarkup(row_width=2)
Is_accepted = InlineKeyboardButton(callback_data='is_accept', text='✅')
Is_not_accepted = InlineKeyboardButton(callback_data='is_not_accept', text='❌')
IsAccept.add(Is_accepted, Is_not_accepted)
