import sqlite3


class Person():
    def __init__(self, user_id: int):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute("SELECT name, money, class, health, stamina, level FROM gameinf WHERE id = ?", (user_id,))
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

    def Update_point(self, user_id, event_point):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute(f"UPDATE gameinf SET money=money+{event_point} WHERE id=?", (user_id,))
        con.commit()
        cur.close()
        con.close()
