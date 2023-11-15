import sqlite3


class VocabularyDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.word_data = self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def create_table(self):
        # create table
        cur = self.conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS vocabulary ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "word TEXT,"
            "definition TEXT,"
            "note TEXT"
            ")"
        )
        self.conn.commit()

        # get data from database and insert them into word_data as dictionary
        cur.execute("SELECT * FROM vocabulary")
        word_data = {}
        for i in cur:
            id = i[0]
            word = i[1]
            definition = i[2]
            note = i[3]
            word_data.update({id: {"word": word, "definition": definition, "note": note}})
        return word_data

    def check_word_exists(self, word):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM vocabulary WHERE word = ?", (word,))
        return cur.fetchone() is not None

    def add_new_word(self, word, definition, note):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO vocabulary (word, definition, note) VALUES (?, ?, ?)",
                        (word, definition, note))
            new_id = cur.lastrowid
            self.conn.commit()
            self.word_data[new_id] = {"word": word, "definition": definition, "note": note}
        except sqlite3.Error:
            self.conn.rollback()
            raise

    def save_data(self):
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM vocabulary")
            for id, info in self.word_data.items():
                cur.execute("INSERT INTO vocabulary (word, definition, note) VALUES (?, ?, ?)",
                            (info["word"], info["definition"], info["note"]))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

    def update_data(self, word):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM vocabulary WHERE word = ?", (word,))
        result = cur.fetchone()
        return result[0]

    def close(self):
        if self.conn:
            self.conn.close()

