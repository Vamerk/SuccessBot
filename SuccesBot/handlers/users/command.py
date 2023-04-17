from aiogram import types
import random
import time

from keyboards.users_board import *
from app import con, cur
from Person import Top_list
from loader import dp, bot
from Person import Person, PvP, Inventory
from data.config import company_chat_id


def check_and_add_user(conn, user_id, username=0):
    isExists = False
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM gameinf WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        isExists = True
        cursor.execute("INSERT INTO gameinf (id, username) VALUES (?, ?)", (user_id, username,))
        conn.commit()
    cursor.close()
    return isExists


def add_inventory(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM inventory WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        isExists = True
        cursor.execute("INSERT INTO inventory (id) VALUES (?)", (user_id,))
        conn.commit()
    cursor.close()


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    add_inventory(con, message.from_user.id)
    if check_and_add_user(con, message.from_user.id, message.from_user.username):
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=first)
    else:
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=second)


@dp.message_handler(commands=['top'])
async def top_users(message: types.Message):
    text = Top_list.rating()
    await bot.send_photo(message.chat.id, photo=open(f'Image/top_users.jpg', 'rb'),
                         caption=f'*🔝Топ пользователей🔝*\n\n'
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
        if not check_and_add_user(con, args, 0):
            pers = Person(args)
            cur.execute("""INSERT INTO PvP (id_attacker, id_deffender) VALUES (?, ?)""",
                        (message.from_user.id, args,))
            con.commit()
            await bot.send_photo(message.chat.id,
                                 photo=open(f'Person_image/user_image/user-{args}.png', 'rb'),
                                 caption=f'Имя: {pers.Name()}\n'
                                         f'Деньги: {pers.Money()}\n'
                                         f'Здоровье: {pers.Health()}\n'
                                         f'Сила: {pers.Stamina()}\n'
                                         f'Уровень: {pers.Level()}\n', reply_markup=Interaction)


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
                                     f'Уровень: {pers.Level()}\n', reply_markup=Pumping)


@dp.callback_query_handler(lambda call: call.data == "attack_on_user")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    await bot.send_message(chat_id=company_chat_id,
                           text=f'Начинается битва между @{Person(PvP().attacking_user()).Username()} и @{Person(PvP().defender_user()).Username()}')
    attack, defend = Person(PvP().attacking_user()), Person(PvP().defender_user())
    at_helth, def_helth = attack.Health(), defend.Health()

    i = 1
    while at_helth >= 0 and def_helth >= 0:
        at_damage, def_damage = attack.Stamina(), defend.Stamina()
        at_damage = round(at_damage * random.uniform(0.75, 1.25), 2)
        def_damage = round(def_damage * random.uniform(0.75, 1.25), 2)
        if i % 2 != 0:  # Удары атакующего
            def_helth -= at_damage
            await bot.send_message(cq.message.chat.id, text=f'{i} Удар\n'
                                                            f'@{attack.Username()} наносит {at_damage} @{defend.Username()}\n\n'
                                                            f'Здоровье @{attack.Username()} : {at_helth}\n'
                                                            f'Здоровье @{defend.Username()} : {def_helth}')
        else:  # Удары защищающегося
            at_helth -= def_damage
            await bot.send_message(cq.message.chat.id, text=f'{i} Удар\n'
                                                            f'@{defend.Username()} наносит {def_damage} @{attack.Username()}\n\n'
                                                            f'Здоровье @{attack.Username()} : {at_helth}\n'
                                                            f'Здоровье @{defend.Username()} : {def_helth}')
        i += 1
        time.sleep(2)

    if at_helth > 0 and def_helth <= 0:
        await bot.send_message(cq.message.chat.id, text=f'Победа за @{attack.Username()}')

    if def_helth > 0 and at_helth <= 0:
        await bot.send_message(cq.message.chat.id, text=f'Победа за @{defend.Username()}')


@dp.callback_query_handler(lambda call: call.data == "share_points_with_user")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    pass
