# Imports
import sqlite3
import time
#from Logging import Logger
# import os
# Globals
# Variable to store the connection object
#db_con = None
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def connect(self):
        if self._connection is None:
            try:
                # Get the current directory of the script
                #current_dir = os.path.dirname(os.path.abspath(__file__))
                # Specify the path to the database file relative to the script
                #db_path = os.path.join(current_dir, '..', 'LibraryDB.sqlite3')
                db_path = "C:/Users/KOM/Documents/Uge 6 - Case 1 - Niveau 2/LibrarySystem/LibraryDB.sqlite3"
                # Connect to SQLite database
                self._connection = sqlite3.connect(db_path)
                print("Connect to DB succesfully")
            except Exception as e:
                print(f"An error occurred when trying to connect to DB, {e}")
        return self._connection

    def close(self):
        if self._connection is not None:
            try:
                # Close database connection
                self._connection.close()
                self._connection = None
                print("Database connection close succesfully")
            except Exception as e:
                print(f"Error occurred when closing the database connection, {e}")

'''
# Example usage - Debug lines
if __name__ == "__main__":
    # This code block will run only if this script is executed directly
    
    # You can put some test code here if needed
    db_connection = DatabaseConnection()
    db_connection.connect()
    time.sleep(5)
    # Test the connection or perform any other operations
    db_connection.close()
'''