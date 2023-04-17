import sqlite3


class PvP:
    def __init__(self):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute("""SELECT id_attacker, id_deffender FROM PvP ORDER BY id_attacker DESC LIMIT 1""")
        self.inform_about_PvP = cur.fetchall()[0]

        cur.close()
        con.close()

    def attacking_user(self):
        return self.inform_about_PvP[0]

    def defender_user(self):
        return self.inform_about_PvP[1]

    def Battle(self):
        return 0

