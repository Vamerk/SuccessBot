from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import random

from aiogram.dispatcher import filters
import logging

from Person import Person
import loader

from other import Event
from app import con, cur
from loader import dp
from data.config import admin_id, company_chat_id
from keyboards.users_board import Go_in_event, IsAccept

bot = loader.bot


# Создаем класс состояний FSM
class EventStates(StatesGroup):
    event_name = State()
    event_discription = State()
    event_points = State()


# Обработчик команды /add_event
@dp.message_handler(commands=["add_event"], chat_id=admin_id)
async def cmd_add_event(message: types.Message):
    # Запускаем FSM и переходим в состояние event_name
    await EventStates.event_name.set()
    await message.answer("Введите название события:")


# Обработчик состояния event_name
@dp.message_handler(state=EventStates.event_name)
async def process_event_name(message: types.Message, state: FSMContext):
    # Сохраняем название события в контекст FSM
    await state.update_data(event_name=message.text)
    # Переходим в состояние event_points
    await EventStates.next()
    await message.answer("Введите описание события:")


@dp.message_handler(state=EventStates.event_discription)
async def process_event_discription(message: types.Message, state: FSMContext):
    # Сохраняем писание события в контекст FSM
    await state.update_data(event_discription=message.text)

    # Переходим в состояние event_points
    await EventStates.next()
    await message.answer("Введите количество очков, которое можно получить за это событие:")


# Обработчик состояния event_points
@dp.message_handler(state=EventStates.event_points)
async def process_event_points(message: types.Message, state: FSMContext):
    # Сохраняем количество очков в контекст FSM
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

    # Отправляем событие в чат
    await bot.send_message(chat_id=-991197527, text=f"Новое событие\n\n"
                                                    f"Название: {event_name}\n"
                                                    f"Описание: {event_discription}\n"
                                                    f"Очки: {event_points}", reply_markup=Go_in_event)

    # Завершаем FSM и переходим в состояние START

    await EventStates.event_name.set()
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == "go_in_event")
async def process_callback_go_in_event(cq: types.CallbackQuery):
    # Event().Update_winners(cq.from_user.id)
    await bot.send_message(admin_id, text=f'User: @{cq.from_user.username}\n'
                                          f'User_id: {cq.from_user.id}\n'
                                          f'Говорит, что выполнил задание, надо проверить!', reply_markup=IsAccept)

    await bot.edit_message_text(chat_id=cq.message.chat.id, message_id=cq.message.message_id,
                                text=f'Пользователь @{cq.from_user.username} выполнил задание\n'
                                     f'Администратор проверит это в ближайшее время')

    cur.execute(f"UPDATE events SET user_id = ? WHERE id = (SELECT MAX(id) FROM events)", (cq.from_user.id,))
    con.commit()



@dp.callback_query_handler(lambda call: call.data == "is_accept")
async def process_callback_is_accept(cq: types.CallbackQuery):
    ev = Event()
    pers = Person(ev.event_user_id())
    await bot.send_message(chat_id=company_chat_id, text=f'Пользователь @{pers.Username()} получает {ev.event_point()} очков ')
    pers.Update_point(ev.event_point())
    pers.add_exp(10)


@dp.callback_query_handler(lambda call: call.data == "is_not_accept")
async def process_callback_is_accept(cq: types.CallbackQuery):
    ev = Event()
    pers = Person(ev.event_user_id())
    await bot.send_message(chat_id=company_chat_id,
                           text=f'Пользователь @{pers.Username()} теряет {ev.event_point()} очков, так как не выполнил задание')
    pers.Update_point(-ev.event_point())
    await bot.send_message(chat_id=company_chat_id, text=f"Новое событие\n\n"
                                                    f"Название: {ev.event_name()}\n"
                                                    f"Описание: {ev.event_discription()}\n"
                                                    f"Очки: {ev.event_point()}", reply_markup=Go_in_event)