from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app import con
from loader import dp

@dp.message_handler()
async def bot_start(message: types.Message):
    pass


""" Схема работы:
Подрубаем машину состояний
Запрашиваем и сохраняем название События
Запрашиваем и сохраняем кол-во очков, которое можно получить за событие
высылаем событие в чат 
"""