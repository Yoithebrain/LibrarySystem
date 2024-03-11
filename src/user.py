import sqlite3
from datetime import datetime

class user:

    def __init__(self, name, address, username, password, isAdmin=False, creationDate=None, lastUpdated=None) -> None:
        self.name = name
        self.address = addressk
        self.username = username
        self.password = password
        self.isAdming= isAdmin
        self.creationDate = creationDate if creationDate else datetime.now()
        self.lastUpdated = lastUpdated if lastUpdated else datetime.now()

    @classmethod
    def save_user(self):
        connection = sqlite3.connect('../LibaryDB.sqlite3')
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO users (name, address, username, password, isAdmin, creationDate, lastUpdated)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (self.name, self.address, self.username, self.password,
            1 if self.isAdmin else 0, self.creationDate, self.lastUpdated))
            
            cursor.commit()
        except Exception as e:
            connection.rollbakc()
            return None
        finally:
            cursor.close()
        return self