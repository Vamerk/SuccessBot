from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app import con
from loader import dp, bot
import keyboards
from Person import NewPerson, Person, Inventory


@dp.message_handler(lambda message: message.text)
async def dd_message(message: types.Message):
    if message.text == 'Получить персонажа👤':
        NewPerson(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'))
        await message.answer(text=f'имя вашего персонажа: {Person(message.from_user.id).Name()}', reply_markup=keyboards.users_board.second)

    if message.text == 'Мой персонаж👤':
        pers = Person(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'),
                             caption=f'👨‍💻Имя: {pers.Name()}\n'
                                     f'💰Деньги: {pers.Money()}\n'
                                     f'💊Здоровье: {pers.Health()}\n'
                                     f'💪Сила: {pers.Stamina()}\n'
                                     f'👾Уровень: {pers.Level()}\n'
                                     f'Опыт: {pers.Exp()}', reply_markup=types.ReplyKeyboardRemove())

    if message.text == '@BotOfSuccess_bot Инвентарь':
        inv = Inventory(message.from_user.id)
        await bot.send_message(message.chat.id, text=f'Гантели: {inv.gantel()}\n'
                                                     f'Кроссовки: {inv.sneakers()}\n'
                                                     f'Ремень: {inv.belt()}\n'
                                                     f'Трусы: {inv.undp()}\n'
                                                     f'Обычный лутбокс: {inv.lootboxs_s()}\n'
                                                     f'Премиальный лутбокс: {inv.lootboxs_p()}\n')

