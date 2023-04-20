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
               username TEXT DEFAULT '',
               status NUMERIC DEFAULT 0, 
               name TEXT DEFAULT '',
               money INTEGER DEFAULT 0, 
               class INTEGER DEFAULT 1, 
               health INTEGER DEFAULT 0, 
               stamina INTEGER DEFAULT 0, 
               level INTEGER DEFAULT 0,
               exp INTEGER DEFAULT 0
               )
    """)
    con.commit()

c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
if c.fetchall() != []:
    c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    print(c.fetchall())
else:
    cur.execute("""
        CREATE TABLE events (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER DEFAULT 0,
               name TEXT DEFAULT "",
               discription TEXT DEFAULT "",
               point INTEGER DEFAULT 0
               )
    """)
    con.commit()

c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PvP'")
if c.fetchall() != []:
    c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PvP'")
    print(c.fetchall())
else:
    cur.execute("""
        CREATE TABLE PvP (
               id_attacker INTEGER,
               id_deffender INTEGER
               )""")
    con.commit()

c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
if c.fetchall() != []:
    c = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
    print(c.fetchall())
else:
    cur.execute("""
        CREATE TABLE inventory (
               id INTEGER PRIMARY KEY,
               gantel INTEGER DEFAULT 0,
               cross NUMERIC DEFAULT 0,
               remen NUMERIC DEFAULT 0,
               undp NUMERIC DEFAULT 0,
               lootboxs_s INTEGER DEFAULT 0,
               lootboxs_p INTEGER DEFAULT 0
               )""")
    con.commit()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
    con.commit()
    con.close()
