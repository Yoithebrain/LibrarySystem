import sqlite3
import logging
from datetime import datetime, timedelta
from Database import DatabaseConnection
from Logging import Logger as log
class BorrowSystem:
    def __init__(self):
        self.db_connection = DatabaseConnection().connect()
    
    # Borrows a book
    @log.log_function_call(level=logging.INFO)
    def borrow_book(self, user_id, book_id):
        try:
            connection = self.db_connection
            cursor = connection.cursor()

            # Check if the book exists in the BorrowedBooks table
            cursor.execute("SELECT isAvailable FROM BorrowedBooks WHERE bookID=?", (book_id,))
            book_status = cursor.fetchone()


            if book_status:  # Book exists in BorrowedBooks table
                if book_status[0] == 1:  # Book is available for borrowing
                    # Get current date and expiry date (7 days from borrow date)
                    borrowDate = datetime.now()
                    
                    expireDate = borrowDate + timedelta(days=7)

                    cursor.execute('''INSERT INTO BorrowedBooks (userID, bookID, dateUpdated, isAvailable, borrowedDate, expireDate, expired) 
                                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                                   (user_id, book_id, borrowDate, 0, borrowDate, expireDate, 0))

                    connection.commit()
                    print("Book borrowed successfully!")
                else:
                    print("Book is not available for borrowing.")
            else:  # Book does not exist in BorrowedBooks table
                # Get current date and expiry date (7 days from borrow date)
                borrowDate = datetime.now()
                expireDate = borrowDate + timedelta(days=7)

                cursor.execute('''INSERT INTO BorrowedBooks (userID, bookID, dateUpdated, isAvailable, borrowedDate, expireDate, expired) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                               (user_id, book_id, borrowDate, 0, borrowDate, expireDate, 0))

                connection.commit()
                print("Book borrowed successfully\n")

        except sqlite3.Error as e:
            log.log_exception(level=logging.CRITICAL, exception=e)
            log.log_exception(level=logging.CRITICAL, exception=e)
            print("Error occurred:", e)
        finally:
            cursor.close()

    # Returns a single book
    @log.log_function_call(level=logging.INFO)
    def return_book(self, user_id, book_id,):
        try:
            connection = self.db_connection
            cursor = connection.cursor()
            current_date = datetime.now()
            # Get borrow due date
            cursor.execute("SELECT expireDate FROM BorrowedBooks WHERE bookID=?", (book_id,))
            borrow_details = cursor.fetchone()
            print(borrow_details)
            if borrow_details:
                # Expire date of borrow entry
                expire_date = borrow_details[0]

                # Convert so we can compare
                expire_date = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S.%f")
            
                if current_date <= expire_date:
                    # Update the BorrowedBooks table to mark the book as returned
                    cursor.execute("UPDATE BorrowedBooks SET deliveredDate=?, isAvailable=?, userID=?, dateUpdated=? WHERE bookID=?", 
                            (current_date, 1,user_id, current_date, book_id))
                    print("Book returned before due date")
                
                else:
                    cursor.execute("UPDATE BorrowedBooks SET deliveredDate=?, isAvailable=?, userID=?, expired=1, dateUpdated=? WHERE bookID=?", 
                            (current_date, 1,user_id, current_date, book_id))
                    print("Book returned after due date! :/")
                self.db_connection.commit()
    
            #print("Book returned successfully.")
        except sqlite3.Error as e:
            log.log_exception(level=logging.ERROR, exception=e)
            log.log_exception(level=logging.ERROR, exception=e)
            print("Error occurred while returning book:", e)
        finally:
            cursor.close()

    # Returns all borrowed books that haven't been returned as of yet
    @log.log_function_call(level=logging.INFO)
    def return_all_books(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            # Get all borrowed books for the user Id
            cursor.execute("SELECT borrowID FROM BorrowedBooks WHERE userID=? AND isAvailable = 0", (user_id,))
            borrowed_books = cursor.fetchall()

            if borrowed_books:
                for borrow_id in borrowed_books:
                    # Return the current book
                    self.return_book(borrow_id[0], user_id)
            else:
                print("User has no borrowed books\n")
        except sqlite3.Error as e:
            log.log_exception(level=logging.ERROR, exception=e)
            print(f"Error occurred when trying to return books: {e}")
        finally:
            cursor.close()

    # Returns all book IDs based on user ID where isAvailable is 0 and deliveredDate is null
    @log.log_function_call(level=logging.INFO)
    def get_borrowed_book_ids(self, user_id):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("SELECT bookID FROM BorrowedBooks WHERE userID=? AND isAvailable=0 AND deliveredDate IS NULL", (user_id,))
            borrowed_book_ids = [row[0] for row in cursor.fetchall()]
            return borrowed_book_ids
        except sqlite3.Error as e:
            log.log_exception(level=logging.ERROR, exception=e)
            print("Error occurred while retrieving borrowed book IDs:", e)
            return []
        finally:
            cursor.close()

    #Gets all bookIDs of unavailable books       
    @log.log_function_call(level=logging.INFO)
    def get_unavailable_books(self):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("SELECT bookID FROM BorrowedBooks WHERE isAvailable = 0 AND deliveredDate IS NULL")
            unavailable_books = [row[0] for row in cursor.fetchall()]
            return unavailable_books
        except sqlite3.Error as e:
            log.log_exception(level=logging.ERROR, exception=e)
            print("Error occurred while retrieving unavailable books:", e)
            return []
        finally:
            cursor.close()
