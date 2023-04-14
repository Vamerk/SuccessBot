from aiogram import types

import keyboards.users_board
from app import con
from Person import Top_list
from loader import dp, bot
from Person import Person


def check_and_add_user(conn, user_id):
    isExists = False
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM gameinf WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        isExists = True
        cursor.execute("INSERT INTO gameinf (id) VALUES (?)", (user_id,))
        conn.commit()
    cursor.close()
    return isExists


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    if check_and_add_user(con, message.from_user.id):
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboards.users_board.first)
    else:
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboards.users_board.second)


@dp.message_handler(commands=['top'])
async def top_users(message: types.Message):
    text = Top_list.rating()
    await bot.send_photo(message.chat.id, photo=open(f'Image/top_users.jpg', 'rb'), caption=f'*🔝Топ пользователей🔝*\n\n'
                                                 f'{text}', parse_mode="MarkDownV2")


@dp.message_handler(commands=['help'])
async def top_users(message: types.Message):
    help_text = f'/start - 🏁Запустить/обновить бота\n' \
                f'/top - 🔥Топ пользователей\n' \
                f'/info - ❗️Информация о своем персонаже\n' \
                f'/info (user_id) - ❗️Информация о чужом персонаже\n' \
                f'/help - ❓Помощь по боту/список команд\n'

    await bot.send_photo(message.chat.id, photo=open(f'Image/help_photo.jpg', 'rb'),
                         caption=f'<b>❗️Список основных команд❗️</b>\n\n'
                                 f'{help_text}', parse_mode="HTML")


@dp.message_handler(commands=['info'])
async def top_users(message: types.Message):
    if message.get_args():
        args = message.get_args()
        if not check_and_add_user(con, args):
            pers = Person(args)
            await bot.send_photo(message.chat.id,
                                 photo=open(f'Person_image/user_image/user-{args}.png', 'rb'),
                                 caption=f'Имя: {pers.Name()}\n'
                                         f'Деньги: {pers.Money()}\n'
                                         f'Здоровье: {pers.Health()}\n'
                                         f'Сила: {pers.Stamina()}\n'
                                         f'Уровень: {pers.Level()}\n', reply_markup=keyboards.users_board.Interaction)


        else:
            await bot.send_message(message.chat.id,
                                   text=f'Такого у нас нет, возможно вы ошиблись. Попробуйте ввести другой ID')

    else:
        pers = Person(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'),
                             caption=f'Имя: {pers.Name()}\n'
                                     f'Деньги: {pers.Money()}\n'
                                     f'Здоровье: {pers.Health()}\n'
                                     f'Сила: {pers.Stamina()}\n'
                                     f'Уровень: {pers.Level()}\n')
