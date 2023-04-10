import sqlite3

async def on_startup(dp):
    print('all ok')


con = sqlite3.connect('gamebase.db')
cur = con.cursor()

c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gameinf'")
if c.fetchall() != []:
    c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gameinf'")
    print(c.fetchall())
else:
    cur.execute("""
        CREATE TABLE gameinf (
               id INTEGER PRIMARY KEY, 
               status NUMERIC DEFAULT 0, 
               name TEXT DEFAULT "",
               money INTEGER DEFAULT 0, 
               class INTEGER DEFAULT 1, 
               health INTEGER DEFAULT 0, 
               stamina INTEGER DEFAULT 0, 
               level INTEGER DEFAULT 0
               )
    """)
    con.commit()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
    con.commit()
    con.close()