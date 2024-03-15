import logging
import traceback
import Database

class Logger:
    def __init__(self):
        self.db_connection = Database.DatabaseConnection().connect()
        self.create_log_table()

    def create_log_table(self):
        # Create the log table if it doesn't exist
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logging (
                    logID INTEGER PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    level VARCHAR(10),
                    message TEXT
                )
            """)

    def log_exception(self, exception, level=logging.ERROR):
        # Log the exception along with traceback information
        traceback_str = traceback.format_exc()
        self.log(level, f"Exception occurred: {exception}\n{traceback_str}")

    @staticmethod
    def log_function_call(func=None, level=logging.INFO):
        def decorator(inner_func):
            def wrapper(*args, **kwargs):
                Logger().log(level=level, message=f"Calling {inner_func.__name__} with args={args}, kwargs={kwargs}")
                return inner_func(*args, **kwargs)
            if isinstance(inner_func, classmethod):
                return inner_func
            else:
                return wrapper
        # Check if the decorator is used with or without arguments
        if func is None:
            return decorator
        else:
            return decorator(func)

    def log(self, level, message):
        # Insert log message into the database
        with self.db_connection:
            self.db_connection.execute("INSERT INTO Logging (level, message) VALUES (?, ?)", (level, message))