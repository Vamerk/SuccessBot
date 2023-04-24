import sqlite3

conn = sqlite3.connect('../gamebase.db', timeout=10)
cursor = conn.cursor()

cursor.execute('SELECT id, name, money FROM gameinf ORDER BY money DESC')

result = cursor.fetchall()

conn.close()

for row in result:
    print(f'{row[0]} - {row[1]}: {row[2]} очков')