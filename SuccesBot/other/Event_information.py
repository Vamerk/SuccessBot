import sqlite3


class Event():
    def __init__(self):
        con = sqlite3.connect('gamebase.db')
        cur = con.cursor()
        cur.execute("SELECT name, user_id, discription, point FROM events ORDER BY id DESC LIMIT 1")
        self.inform_about_event = cur.fetchone()
        cur.close()
        con.close()

    # def Update_winners(self, user_id):
    #     con = sqlite3.connect('gamebase.db')
    #     cur = con.cursor()
    #     c = cur.execute("UPDATE events SET user_id=? WHERE id = (SELECT MAX(id) FROM events)", (user_id,))
    #     print(c.fetchall())
    #     con.commit()
    #     cur.close()
    #     con.close()

    def event_name(self):
        return self.inform_about_event[0]

    def event_user_id(self):
        return self.inform_about_event[1]

    def event_discription(self):
        return self.inform_about_event[2]

    def event_point(self):
        return self.inform_about_event[3]
