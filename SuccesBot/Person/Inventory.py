import sqlite3

class Inventory:
    def __init__(self, user_id: int):
        con = sqlite3.connect('gamebase.db', timeout=10)
        cur = con.cursor()
        cur.execute("SELECT gantel, cross, remen, undp, lootboxs_s, lootboxs_p FROM inventory WHERE id = ?", (user_id,))
        self.inventory_info = cur.fetchone()
        print(self.inventory_info)
        cur.close()
        con.close()

    def gantel(self): return self.inventory_info[0]

    def sneakers(self): return self.inventory_info[1]

    def belt(self): return self.inventory_info[2]

    def undp(self): return self.inventory_info[3]

    def lootboxs_s(self): return self.inventory_info[4]

    def lootboxs_p(self): return self.inventory_info[5]
