from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import random
import time

from aiogram.dispatcher import filters
import logging

from Person import Person
from other import send_lootbox
import loader

from other import Event
from app import con, cur
from loader import dp
from data.config import admin_id, company_chat_id
from keyboards.users_board import Go_in_event, IsAccept

bot = loader.bot


class EventStates(StatesGroup):
    event_name = State()
    event_discription = State()
    event_points = State()



@dp.message_handler(commands=["add_event"], chat_id=admin_id)
async def cmd_add_event(message: types.Message):
    # Запускаем FSM и переходим в состояние event_name
    await EventStates.event_name.set()
    await message.answer("Введите название события:")


# Обработчик состояния event_name
@dp.message_handler(state=EventStates.event_name)
async def process_event_name(message: types.Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await EventStates.next()
    await message.answer("Введите описание события:")


# Обработчик состояния event_discription
@dp.message_handler(state=EventStates.event_discription)
async def process_event_discription(message: types.Message, state: FSMContext):
    await state.update_data(event_discription=message.text)

    await EventStates.next()
    await message.answer("Введите количество очков, которое можно получить за это событие:")


# Обработчик состояния event_points
@dp.message_handler(state=EventStates.event_points)
async def process_event_points(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event_name = data.get("event_name")
    event_discription = data.get("event_discription")
    event_points = message.text

    await message.answer(f"Событие создано\n\n"
                         f"Название: {event_name}\n"
                         f"Описание: {event_discription}\n"
                         f"Очки: {event_points}")

    # Записываем событие в БД
    c = cur.execute("INSERT INTO events (name, discription, point) VALUES (?, ?, ?)",
                    (event_name, event_discription, event_points,))
    print(c.fetchall())
    con.commit()

    await bot.send_message(chat_id=-991197527, text=f"Новое событие\n\n"
                                                    f"Название: {event_name}\n"
                                                    f"Описание: {event_discription}\n"
                                                    f"Очки: {event_points}", reply_markup=Go_in_event)

    await EventStates.event_name.set()
    await state.finish()


# Юзер нажал кнопку вступления в событие
@dp.callback_query_handler(lambda call: call.data == "go_in_event")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    await bot.send_message(admin_id, text=f'User: @{cq.from_user.username}\n'
                                          f'User_id: {cq.from_user.id}\n'
                                          f'Говорит, что выполнил задание, надо проверить!', reply_markup=IsAccept)

    await bot.edit_message_text(chat_id=company_chat_id, message_id=cq.message.message_id,
                                text=f'Пользователь @{cq.from_user.username} выполнил задание\n'
                                     f'Администратор проверит это в ближайшее время')

    cur.execute(f"UPDATE events SET user_id = ? WHERE id = (SELECT MAX(id) FROM events)", (cq.from_user.id,))
    con.commit()


# Админ подтвердил выполнение события
@dp.callback_query_handler(lambda call: call.data == "is_accept")
async def process_callback_is_accept(cq: types.CallbackQuery):
    ev = Event()
    pers = Person(ev.event_user_id())
    if int(await send_lootbox(ev.event_user_id())) > 0: await bot.send_message(company_chat_id, text=f'Выпал лутбокс!!')
    await bot.send_message(company_chat_id, text=f'Пользователь @{pers.Username()} получает {ev.event_point()} очков ')
    pers.Update_point(ev.event_point())
    pers.add_exp(10)

# Админ не подтвердил выполнение события
@dp.callback_query_handler(lambda call: call.data == "is_not_accept")
async def process_callback_is_accept(cq: types.CallbackQuery):
    ev = Event()
    pers = Person(ev.event_user_id())
    await bot.send_message(cq.message.chat.id,
                           text=f'Пользователь @{pers.Username()} теряет {ev.event_point()} очков, так как не выполнил задание')
    pers.Update_point(-ev.event_point())
    await bot.send_message(cq.message.chat.id, text=f"Новое событие\n\n"
                                                    f"Название: {ev.event_name()}\n"
                                                    f"Описание: {ev.event_discription()}\n"
                                                    f"Очки: {ev.event_point()}", reply_markup=Go_in_event)





