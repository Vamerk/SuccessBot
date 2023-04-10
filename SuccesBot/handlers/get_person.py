from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app import con
from loader import dp, bot

from Person import NewPerson, Person


@dp.message_handler(lambda message: message.text)
async def dd_message(message: types.Message):
    if message.text == 'Получить персонажа👤':
        NewPerson(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'))
        await message.answer(text=f'имя вашего персонажа: {Person(message.from_user.id).Name()}')

    if message.text == 'Мой персонаж👤':
        pers = Person(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'),
                             caption=f'Имя: {pers.Name()}\n'
                                     f'Деньги: {pers.Money()}\n'
                                     f'Здоровье: {pers.Health()}\n'
                                     f'Сила: {pers.Stamina()}\n'
                                     f'Уровень: {pers.Level()}\n', reply_markup=types.ReplyKeyboardRemove())
