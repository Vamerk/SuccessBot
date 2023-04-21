import sqlite3


class Person():
    def __init__(self, user_id: int):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        self.user_id = user_id
        cur.execute("SELECT name, money, class, health, stamina, level, username, exp FROM gameinf WHERE id = ?", (user_id,))
        self.inform_about_person = cur.fetchone()
        cur.close()
        con.close()

    def Name(self):
        return self.inform_about_person[0]

    def Money(self):
        return self.inform_about_person[1]

    def Class(self):
        return self.inform_about_person[2]

    def Health(self):
        return self.inform_about_person[3]

    def Stamina(self):
        return self.inform_about_person[4]

    def Level(self):
        return self.inform_about_person[5]

    def Username(self):
        return self.inform_about_person[6]

    def Exp(self):
        return self.inform_about_person[7]

    def Update_point(self, event_point):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute(f"UPDATE gameinf SET money=money+{event_point} WHERE id=?", (self.user_id,))
        con.commit()
        cur.close()
        con.close()

    def add_exp(self, get_exp):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute(f"UPDATE gameinf SET exp=exp+{get_exp} WHERE id=?", (self.user_id,))
        con.commit()
        cur.close()
        con.close()

    def LevelUp(self):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute(f"UPDATE gameinf SET exp=0, level=level+1, health=health+5, stamina=stamina+2.5 WHERE id=?", (self.user_id,))
        con.commit()
        cur.close()
        con.close()