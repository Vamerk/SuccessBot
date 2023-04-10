from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app import con
from loader import dp

from Person import Person

@dp.message_handler(commands=['info'])
async def bot_start(message: types.Message):
    await message.answer(f'ваш персонаж:, {Person(message.from_user.id).Name()}'
                         f'{Person(message.from_user.id).Money()}'
                         f'{Person(message.from_user.id).Level()}')
