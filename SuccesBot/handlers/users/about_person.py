from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app import con
from loader import dp, bot
from keyboards.users_board import *
from Person import NewPerson, Person, Inventory
from other import open_standart_lootbox, open_premium_lootbox
import time


@dp.message_handler(lambda message: message.text)
async def dd_message(message: types.Message):
    if message.text == 'Получить персонажа👤':
        NewPerson(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'))
        await message.answer(text=f'имя вашего персонажа: {Person(message.from_user.id).Name()}', reply_markup=second)

    if message.text == 'Мой персонаж👤':
        pers = Person(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'),
                             caption=f'👨‍💻Имя: {pers.Name()}\n'
                                     f'💰Очки: {pers.Money()}\n'
                                     f'💊Здоровье: {pers.Health()}\n'
                                     f'💪Сила: {pers.Stamina()}\n'
                                     f'👾Уровень: {pers.Level()}\n'
                                     f'⭐️Опыт: {pers.Exp()}', reply_markup=types.ReplyKeyboardRemove())

    if message.text == '@BotOfSuccess_bot Инвентарь':
        inv = Inventory(message.from_user.id)
        await bot.send_message(message.chat.id, text=f'🏋‍♂Гантели: {inv.gantel()}\n'
                                                     f'👟Кроссовки: {inv.sneakers()}\n'
                                                     f'🥇Пояс: {inv.belt()}\n'
                                                     f'🩲Трусы: {inv.undp()}\n'
                                                     f'📦Обычный лутбокс: {inv.lootboxs_s()}\n'
                                                     f'🎁Премиальный лутбокс: {inv.lootboxs_p()}\n', reply_markup=Inventory_menu)

    if message.text == '@BotOfSuccess_bot Повысить уровень':
        pers = Person(message.from_user.id)
        if pers.Exp() >= pers.Level() * 100:
            pers.LevelUp()
            await bot.send_message(message.chat.id, text=f'Уровень повышен, теперь ваш персонаж {pers.Level()+1} уровня')
        else: await bot.send_message(message.chat.id, text=f'Не хватает опыта😕')

    if message.text == '@BotOfSuccess_bot Открыть лутбокс':
        if int(Inventory(message.from_user.id).lootboxs_s()) >= 1:
            await bot.send_animation(message.chat.id, animation=open(f'Image/open_lootbox.gif.mp4', 'rb'))
            time.sleep(2)
            await bot.delete_message(message.chat.id, message_id=message.message_id+1)

            await bot.send_message(message.chat.id, text=f'🎊Вам выпадает: '
                                                         f'\n{open_standart_lootbox(message.from_user.id)}')
        else:
            await bot.send_message(message.chat.id, text=f'У вас нет боксов😕')

    if message.text == '@BotOfSuccess_bot Открыть премиум лутбокс':
        if int(Inventory(message.from_user.id).lootboxs_p()) >= 1:
            await bot.send_animation(message.chat.id, animation=open(f'Image/open_lootbox.gif.mp4', 'rb'))
            time.sleep(2)
            await bot.delete_message(message.chat.id, message_id=message.message_id + 1)

            await bot.send_message(message.chat.id, text=f'🎊Вам выпадает: '
                                                         f'\n{open_premium_lootbox(message.from_user.id)}')
        else:
            await bot.send_message(message.chat.id, text=f'У вас нет боксов😕')