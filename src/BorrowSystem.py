import sqlite3
from datetime import datetime, timedelta
from Database import DatabaseConnection

class BorrowSystem:
    def __init__(self):
        self.db_connection = DatabaseConnection().connect()

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
                print("Book borrowed successfully!")

        except sqlite3.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
    #WIP
    def return_book(self, borrow_id, user_id):
        try:
            cursor = self.db_connection.cursor()
            current_date = datetime.now()
            
            # Update the BorrowedBooks table to mark the book as returned
            cursor.execute("UPDATE BorrowedBooks SET deliveredDate=?, isAvailable=1, userID=? WHERE borrowID=?", 
                           (current_date, user_id, borrow_id))
            self.db_connection.commit()
            print("Book returned successfully.")
        except sqlite3.Error as e:
            print("Error occurred while returning book:", e)
        finally:
            cursor.close()


# Testing borrowing system and if book is already borrowed to be deleted
if __name__ == "__main__":
    book_borrowing_system = BorrowSystem()

    # Example user and book IDs
    user_id = 1
    book_id = 1

    book_borrowing_system.borrow_book(user_id, book_id)
