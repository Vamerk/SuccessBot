from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


first = ReplyKeyboardMarkup(resize_keyboard=True)
getPers = KeyboardButton('Получить персонажа👤')
first.row(getPers)

second = ReplyKeyboardMarkup(resize_keyboard=True)
getPersInfo = KeyboardButton('Мой персонаж👤')
second.row(getPersInfo)