####
# Logs system info to database, useful for keeping track of where issues might occur
# - CLY 14-03-24 -
####
# Imports
#import Database
#import sqlite3
import logging
import Database

class Logger:
    def __init__(self):
        self.db_connection = Database.DatabaseConnection().connect()
        self.con = self.db_connection
        self.create_log_table()

    def create_log_table(self):
        # Create the log table if it doesn't exist
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS logging (
                logID INTEGER PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level VARCHAR(10),
                message TEXT
            )
        """)
        self.con.commit()

    def log_function_call(self, level=logging.INFO):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Log the function call
                self.log(level, f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

                # Call the original function
                result = func(*args, **kwargs)

                return result

            return wrapper

        return decorator

    def log(self, level, message):
        # Insert log message into the database
        self.con.execute("INSERT INTO Logging (level, message) VALUES (?, ?)", (level, message))
        self.con.commit()

    def close_connection(self):
        self.con.close()

'''
# Example usage
if __name__ == "__main__":
    # Create a logger instance
    logger = Logger()

    # Decorator for logging function calls at different levels
    @logger.log_function_call(level=logging.DEBUG)
    def example_function(x, y):
        return x + y

    # Call the decorated function
    result = example_function(3, 5)
    print("Result:", result)
'''