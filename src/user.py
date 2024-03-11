import sqlite3
from datetime import datetime

class user:

    def __init__(self, name, address, username, password, isAdmin=False, creationDate=None, lastUpdated=None) -> None:
        self.name = name
        self.address = address
        self.username = username
        self.password = password
        self.isAdming= isAdmin
        self.creationDate = creationDate if creationDate else datetime.now()
        self.lastUpdated = lastUpdated if lastUpdated else datetime.now()

    @classmethod
    def save_user(self):
        try:
            connection = sqlite3.connect('../LibaryDB.sqlite3')
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO users (name, address, username, password, isAdmin, creationDate, lastUpdated)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (self.name, self.address, self.username, self.password,
            1 if self.isAdmin else 0, self.creationDate, self.lastUpdated))
            
            cursor.commit()
        except sqlite3.Error as e:
            connection.rollbakc()
            print("Error occured:", e)
        finally:
            cursor.close()

    @classmethod
    def load_from_database(cls, username):
        try:
            connection = sqlite3.connect('../LibaryDB.sqlite3')
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user_data = cursor.fetchone()

            if user_data:
                return cls(*user_data[:6], creationDate=datetime.strptime(user_data[6], "%Y-%m-%d %H:%M:%S"),
                           lastUpdated=datetime.strptime(user_data[7], "%Y-%m-%d %H:%M:%S"))
            else:
                return None
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return None
        finally:
            cursor.close()
    
    @classmethod
    def update_in_database(self):
        try:
            connection = sqlite3.connect('../LibaryDB.sqlite3')
            cursor = connection.cursor()

            cursor.execute('''UPDATE users SET name=?, address=?, password=?, isAdmin=?, lastUpdated=?
                         WHERE username=?''',
                      (self.name, self.address, self.password, 1 if self.isAdmin else 0,
                       self.lastUpdated, self.username))

            cursor.commit()
        except sqlite3.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()

    @classmethod
    def delete_from_database(self):
        try:
            connection = sqlite3.connect('../LibaryDB.sqlite3')
            cursor = connection.cursor()

            cursor.execute("DELETE FROM users WHERE username=?", (self.username,))

            cursor.commit()
        except sqlite3.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
    
    @classmethod
    def get_all_users(cls):
        connection = sqlite3.connect('../LibaryDB.sqlite3')
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM users")
            users_data = connection.fetchall()

            users = []
            for user_data in users_data:
                users.append(cls(*user_data[:6], creationDate=datetime.strptime(user_data[6], "%Y-%m-%d %H:%M:%S"),
                            lastUpdated=datetime.strptime(user_data[7], "%Y-%m-%d %H:%M:%S")))
            return users
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return []
        finally:
            connection.close()

        