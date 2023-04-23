from aiogram import types
import random
import time

from keyboards.users_board import *
from app import con, cur
from Person import Top_list
from loader import dp, bot
from Person import Person, PvP, Inventory
from data.config import company_chat_id
from other import send_lootbox


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
                                 f'{text}', parse_mode="markdown")


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
            pers = Person(int(args))
            cur.execute("""INSERT INTO PvP (id_attacker, id_deffender) VALUES (?, ?)""",
                        (message.from_user.id, args,))
            con.commit()
            await bot.send_photo(message.chat.id,
                                 photo=open(f'Person_image/user_image/user-{args}.png', 'rb'),
                                 caption=f'👨‍💻Имя: {pers.Name()}\n'
                                         f'💰Очки: {pers.Money()}\n'
                                         f'💊Здоровье: {pers.Health()}\n'
                                         f'💪Сила: {round(pers.Stamina(), 2)}\n'
                                         f'👾Уровень: {pers.Level()}\n'
                                         f'⭐️Опыт: {pers.Exp()}', reply_markup=Interaction)


        else:
            await bot.send_message(message.chat.id,
                                   text=f'Такого у нас нет, возможно вы ошиблись. Попробуйте ввести другой ID')

    else:
        pers = Person(message.from_user.id)
        await bot.send_photo(message.chat.id,
                             photo=open(f'Person_image/user_image/user-{message.from_user.id}.png', 'rb'),
                             caption=f'👨‍💻Имя: {pers.Name()}\n'
                                     f'💰Очки: {pers.Money()}\n'
                                     f'💊Здоровье: {pers.Health()}\n'
                                     f'💪Сила: {round(pers.Stamina(), 2)}\n'
                                     f'👾Уровень: {pers.Level()}\n'
                                     f'⭐️Опыт: {pers.Exp()}', reply_markup=Pumping)


@dp.callback_query_handler(lambda call: call.data == "attack_on_user")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    random_k = random.uniform(0.10, 0.65)
    attack, defend = Person(PvP().attacking_user()), Person(PvP().defender_user())
    at_helth, def_helth = attack.Health(), defend.Health()
    await bot.send_animation(cq.message.chat.id, animation=open(f'Image/fight.gif', 'rb'),
                             caption=f'Начинается битва между \n@{attack.Username()} и @{defend.Username()}')

    i = 1
    while at_helth > 0 and def_helth > 0:
        at_damage, def_damage = attack.Stamina(), defend.Stamina()
        at_damage = round(at_damage * random.uniform(0.70, 1.30), 2)
        def_damage = round(def_damage * random.uniform(0.70, 1.30), 2)
        if i % 2 != 0:  # Удары атакующего
            def_helth -= at_damage
            msg_id = await bot.send_message(cq.message.chat.id, text=f'{i} Удар\n'
                                                                     f'@{attack.Username()} наносит {at_damage} @{defend.Username()}\n\n'
                                                                     f'Здоровье @{attack.Username()} : {max(0, round(at_helth, 2))}\n'
                                                                     f'Здоровье @{defend.Username()} : {max(0, round(def_helth, 2))}')
        else:  # Удары защищающегося
            at_helth -= def_damage
            msg_id = await bot.send_message(cq.message.chat.id, text=f'{i} Удар\n'
                                                                     f'@{defend.Username()} наносит {def_damage} @{attack.Username()}\n\n'
                                                                     f'Здоровье @{attack.Username()} : {max(0, round(at_helth, 2))}\n'
                                                                     f'Здоровье @{defend.Username()} : {max(0, round(def_helth, 2))}')
        time.sleep(2)
        await bot.delete_message(cq.message.chat.id, message_id=msg_id.message_id)
        i += 1

    if at_helth > 0 and def_helth <= 0:  # Победил атакующий
        await bot.send_message(cq.message.chat.id,
                               text=f'Победа за @{attack.Username()}, он получает {round(defend.Money() * random_k)} очков и {round(10 * (random_k + 1))} опыта')
        # Обновление данных БД
        attack.Update_point(round(defend.Money() * random_k))
        defend.Update_point(-round(defend.Money() * random_k))
        attack.add_exp(round(10 * (random_k + 1)))
        defend.add_exp(round(2))
        if int(await send_lootbox(attack.user_id)) > 0:
            await bot.send_message(cq.message.chat.id, text=f'🎉Выпал лутбокс!!')

    if def_helth > 0 and at_helth <= 0:  # Победил защищающийся
        await bot.send_message(cq.message.chat.id,
                               text=f'Победа за @{defend.Username()}, он получает {round(attack.Money() * random_k)} очков и {round(10 * (random_k + 1))} опыта')
        # Обновление данных БД
        defend.Update_point(round(attack.Money() * random_k))
        attack.Update_point(-round(attack.Money() * random_k))
        defend.add_exp(round(10 * (random_k + 1)))
        attack.add_exp(round(2))
        if int(await send_lootbox(attack.user_id)) > 0: await bot.send_message(cq.message.chat.id,
                                                                               text=f'🎉Выпал лутбокс!!')

    PvP().end_battle()


@dp.callback_query_handler(lambda call: call.data == "share_points_with_user")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    sender = Person(PvP().attacking_user())
    address = Person(PvP().defender_user())
    random_k = random.uniform(0.05, 0.15)
    await bot.send_message(cq.message.chat.id,
                           text=f'@{sender.Username()} отправил {round(sender.Money() * random_k)} очков @{address.Username()}')
    sender.Update_point(-round(sender.Money() * random_k))
    address.Update_point(round(sender.Money() * random_k))
