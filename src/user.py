import sqlite3
from datetime import datetime
import logging

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

    @classmethod
    def save_user(cls, user):
        try:
            connection = sqlite3.connect('../LibraryDB.sqlite3')
            cursor = connection.cursor()
            
            cursor.execute('''INSERT INTO Users (name, address, username, password, isAdminFLG, creationDate, lastUpdated)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user.name, user.address, user.username, user.password,
            1 if user.isAdmin else 0, user.creationDate, user.lastUpdated))
            
            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            print("Error occured:", e)
        finally:
            cursor.close()

    @classmethod
    def load_user(cls, username):
        try:
            connection = sqlite3.connect('../LibraryDB.sqlite3')
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
            user_data = cursor.fetchone()

            if user_data:
                return cls(user_data[1], user_data[2], user_data[3], user_data[4], bool(user_data[5]),
                             user_data[6], user_data[7])
            else:
                return None
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return None
        finally:
            cursor.close()
    
    @classmethod
    def update_user(cls, user):
        try:
            user.lastUpdated = datetime.now()
            logging.info("Updating user: {}".format(user.username))  # Debug statement
            logging.info("New name: {}".format(user.name))  # Debug statement
            connection = sqlite3.connect('../LibraryDB.sqlite3')
            cursor = connection.cursor()

            sql_query = '''UPDATE Users SET name=?, address=?, password=?, isAdminFLG=?, lastUpdated=?
                        WHERE username=?'''
            cursor.execute(sql_query, (user.name, user.address, user.password, 1 if user.isAdmin else 0,
                                    user.lastUpdated, user.username,))

            connection.commit()
            logging.info("User '{}' updated successfully.".format(user.username))
            logging.info("Updated user name: {}".format(user.name))  # Debug statement
            return user
        except sqlite3.Error as e:
            logging.error("Error occurred while updating user '{}': {}".format(user.username, e))
            return None  # Return None in case of an error
        finally:
            cursor.close()
            connection.close()



    @classmethod
    def delete_user(cls, username):
        try:
            connection = sqlite3.connect('../LibraryDB.sqlite3')
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
            connection = sqlite3.connect('../LibraryDB.sqlite3')
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Users")
            users_data = cursor.fetchall()

            users = []
            for user_data in users_data:
                users.append(cls(user_data[1], user_data[2], user_data[3], user_data[4], bool(user_data[5]),
                             user_data[6], user_data[7]))
        
            return users
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return []
        finally:
            connection.close()

# Test the database connection within functions
def test_database_connection():
    logging.info("Testing database connection...")
    try:
        conn = sqlite3.connect('../LibraryDB.sqlite3')
        conn.close()
        logging.info("Database connection successful!")
    except sqlite3.Error as e:
        logging.error("Error occurred while connecting to the database: {}".format(e))

test_database_connection() 

# Examples:
# Creating a new user
new_user = user("Admin", "123 Main St", "johndoe", "password123", isAdmin=True)
user.save_user(new_user)

# Load user
loaded_user = user.load_user("johndoe")
print("Before update:", loaded_user.name, loaded_user.username, loaded_user.isAdmin) 

# Update user
loaded_user.name = "janedoe"
print(loaded_user.name, loaded_user.username)
updated_user = user.update_user(loaded_user)
newLoad_user = user.load_user("janedoe")
print("New load:", newLoad_user.name, newLoad_user.username, newLoad_user.isAdmin)

# After update user
if updated_user:
    print("After update:", updated_user.name, updated_user.username, updated_user.isAdmin)
else:
    print("User 'janedoe' not found in the database.")



# Deleting user
#user.delete_user("johndoe")

# Get all users
#all_users = user.get_all_users()
#for user in all_users:
    #print(user.name,user.lastUpdated)       