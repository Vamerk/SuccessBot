from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# ----------------------------------------------------Кнопки Персонажей
first = ReplyKeyboardMarkup(resize_keyboard=True)
getPers = KeyboardButton('Получить персонажа👤')
first.row(getPers)

second = ReplyKeyboardMarkup(resize_keyboard=True)
getPersInfo = KeyboardButton('Мой персонаж👤')
second.row(getPersInfo)

# ----------------------------------------------------Кнопки для участия в Событиях
Go_in_event = InlineKeyboardMarkup(row_width=1)
Accept_event = InlineKeyboardButton(callback_data='go_in_event', text="✅")
NotAccept_event = InlineKeyboardButton(callback_data='not_in_event', text="❌")
Go_in_event.add(Accept_event)

IsAccept = InlineKeyboardMarkup(row_width=2)
Is_accepted = InlineKeyboardButton(callback_data='is_accept', text='✅')
Is_not_accepted = InlineKeyboardButton(callback_data='is_not_accept', text='❌')
IsAccept.add(Is_accepted, Is_not_accepted)


#-------------------------------------------------PvP(типо)
Interaction = InlineKeyboardMarkup(row_width=1)

Attack = InlineKeyboardButton(callback_data='attack_on_user', text='🫵Вызвать на бой')
Share_points = InlineKeyboardButton(callback_data='share_points_with_user', text='Поделиться очками🤝')
Interaction.add(Attack, Share_points)

#------------------------------------------------------Прокачка персонажа
Pumping = InlineKeyboardMarkup(row_width=1)
Inventory = InlineKeyboardButton('Инвентарь', switch_inline_query_current_chat='Инвентарь')
Up_Level = InlineKeyboardButton('Повысить уровень', switch_inline_query_current_chat='Повысить уровень')
Pumping.add(Inventory, Up_Level)