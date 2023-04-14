import sqlite3
import random

emodji = '😎🙈😅🤗🫡😵‍👽🐵🌚🗿😂😇🤪🧐🤨🤩🥳🤯🤬🥵🤫🤭🥴'


def rating():
    text = ''
    conn = sqlite3.connect('gamebase.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, money FROM gameinf ORDER BY money DESC LIMIT 10')

    result = cursor.fetchall()

    conn.close()

    for row in result:
        r = random.choice(emodji)
        text += f'{r}`{row[0]}`: {row[1]} очков\n'

    return text
