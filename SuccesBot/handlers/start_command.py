from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import keyboards.users_board
from app import con
from loader import dp

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

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if check_and_add_user(con, message.from_user.id):
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboards.users_board.first)
    else:
        await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboards.users_board.second)
