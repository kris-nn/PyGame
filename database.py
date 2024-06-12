import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('scores.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS scores
                         (name TEXT, score INTEGER)''')

    def save_score(self, name, score):
        self.c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()

    def get_top_scores(self):
        self.c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
        return self.c.fetchall()
