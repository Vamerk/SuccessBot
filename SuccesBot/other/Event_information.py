import sqlite3


class Event():
    def __init__(self):
        con = sqlite3.connect('gamebase.db', timeout=10)
        cur = con.cursor()
        cur.execute("SELECT name, user_id, discription, point FROM events ORDER BY id DESC LIMIT 1")
        self.inform_about_event = cur.fetchone()
        cur.close()
        con.close()

    def event_name(self):
        return self.inform_about_event[0]

    def event_user_id(self):
        return self.inform_about_event[1]

    def event_discription(self):
        return self.inform_about_event[2]

    def event_point(self):
        return self.inform_about_event[3]
