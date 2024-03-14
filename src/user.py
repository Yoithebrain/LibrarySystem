import sqlite3
from datetime import datetime
import logging
from Database import DatabaseConnection

logging.basicConfig(level=logging.INFO) 
class user:

    def __init__(self, name, address, username, password, isAdmin=False, creationDate=None, lastUpdated=None) -> None:
        self.name = name
        self.address = address
        self.username = username
        self.password = password
        self.isAdmin= isAdmin
        self.creationDate = creationDate if creationDate else datetime.now()
        self.lastUpdated = lastUpdated if lastUpdated else datetime.now()

    def verify_password(self, password):
        return self.password == password    

    @classmethod
    def save_user(cls, user):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute('''INSERT INTO Users (name, address, username, password, isAdminFLG, creationDate, lastUpdated)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user.name, user.address, user.username, user.password,
            1 if user.isAdmin else 0, user.creationDate, user.lastUpdated))

            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            print("Error occurred:", e)
        finally:
            cursor.close()

    @classmethod
    def load_user(cls, username):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
            user_data = cursor.fetchone()

            if user_data:
                user_id = user_data[0]
                user_obj = cls(user_data[3], user_data[4], user_data[1], user_data[2], bool(user_data[5]), user_data[6], user_data[7])
                return user_id, user_obj
            else:
                return None
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return None
        finally:
            cursor.close()

    @classmethod
    def update_user(cls, username, user):
        try:
            user.lastUpdated = datetime.now()

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            sql_query = '''UPDATE Users SET name=?, address=?, username=?,password=?, isAdminFLG=?, lastUpdated=?
                        WHERE username=?'''
            cursor.execute(sql_query, (user.name, user.address, user.username, user.password, 1 if user.isAdmin else 0,
                                    user.lastUpdated, username))

            connection.commit()
            logging.info("User '{}' updated successfully.".format(user.username))
            return user
        except sqlite3.Error as e:
            logging.error("Error occurred while updating user '{}': {}".format(user.username, e))
            return None
        finally:
            cursor.close()

    @classmethod
    def delete_user(cls, username):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Users WHERE username=?", (username,))

            connection.commit()
        except sqlite3.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()

    @classmethod
    def get_all_users(cls):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Users")
            users_data = cursor.fetchall()

            users = []
            for user_data in users_data:
                user = {
                    "userID": user_data[0],
                    "name": user_data[3],
                    "address": user_data[4],
                    "username": user_data[1],
                    "password": user_data[2],
                    "isAdmin": bool(user_data[5]),
                    "creationDate": user_data[6],
                    "lastUpdated": user_data[7]
                }
                users.append(user)

            return users
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return []
        finally:
            cursor.close

# Test the database connection within functions
def test_database_connection():
    logging.info("Testing database connection...")
    try:
        DatabaseConnection().connect()
        logging.info("Database connection successful!")
    except sqlite3.Error as e:
        logging.error("Error occurred while connecting to the database: {}".format(e))

#test_database_connection() 

# Examples:
# Creating a new user
#new_user = user("Admin", "123 Main St", "johndoe", "password123", isAdmin=True)
#user.save_user(new_user)

# Load user
#loaded_user = user.load_user("janedoe")
#print("Before update:", "name:" ,loaded_user.name,"username:" ,loaded_user.username, "isAdmin:", loaded_user.isAdmin) 

# Update user
#old_username = loaded_user.username # Look up in db based on old username
#loaded_user.name = "AdminUpdate2" # changes name
#loaded_user.username = "janedoe" # changes username

#updated_user = user.update_user(username=old_username,user=loaded_user) # can update multiple fields

# Deleting user
#user.delete_user("johndoe")

# Get all users
#all_users = user.get_all_users()
#for user in all_users:
    #print(user)       