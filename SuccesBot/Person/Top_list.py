import sqlite3

def rating():
    text = ''
    conn = sqlite3.connect('gamebase.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, money FROM gameinf ORDER BY money DESC LIMIT 10')

    result = cursor.fetchall()

    conn.close()

    for row in result:
        text += f'{row[0]} - {row[1]}: {row[2]} очков\n'

    return text
