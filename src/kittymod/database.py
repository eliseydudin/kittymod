import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("kittymod.db", autocommit=True)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS strikes(id INT, strikes INT)"
        )

    def __del__(self):
        self.connection.close()

    def add_strikes(self, id: int) -> int:
        cursor = self.connection.cursor()

        cursor.execute("SELECT strikes FROM strikes WHERE id=? LIMIT 1", (id,))
        strikes = cursor.fetchone()[0]
        if strikes is None:
            self.connection.execute("INSERT INTO strikes VALUES(?, ?)", (id, 1))
            return 1
        strikes += 1

        self.connection.execute(
            "UPDATE strikes SET strikes=? WHERE id=?", (strikes, id)
        )

        cursor.close()

        return strikes
