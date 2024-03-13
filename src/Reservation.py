####
# Handles reservations
# - CLY 13-03-24 -
####
# Imports
import sqlite3
import Database
import datetime

# Class definition
class Reservation:
    def __init__(self, conn):
        self.conn = conn
    ####
    # Function that deals with reserving a book, currently a book can only be reserved once. This is a limitation from our side to prevent issue with
    # multiple active reservations.. As that would mean a different setup for the current database.
    # - CLY 13-03-24 - 
    ####
    def reserve_book(self, user_id, book_id):
        try:
            cursor = self.conn.cursor()
            # Check if a reservation already exists
            cursor.execute("SELECT COUNT(*) FROM Reservations WHERE bookID = ? AND isFulfilled = 0", (book_id,))
            active_res_count = cursor.fetchone()[0]
            if active_res_count == 0:
                reservationDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO Reservations (userID, bookID, reservationDate) VALUES (?, ?, ?)", (user_id, book_id, reservationDate))
                self.conn.commit()
                print("Book has been reserved")
            else:
                print("There is already an active reservation for the book in the system currently, please try again at another time")
        except Exception as e:
            print(f"Something went wrong when trying to reserve the book, {e}")
    
    ###
    # Checks if a book have been returned where the book may have a reservation
    # - CLY 13-03-24 -
    ###
    def check_reservation_availbility (self, book_id):
        try:
            cursor = self.conn.cursor()
            # Check if the book is currently being borrowed or if the book have been returned
            cursor.execute("SELECT COUNT(*) FROM BorrowedBooks WHERE bookID = ? and isAvailable = 1", (book_id,))
            res_count = cursor.fetchone()[0]
            if res_count == 0:
                print("Reservation is available")
                #return res
            else:
                print("Book is still not available")
        except sqlite3.Error as e:
            print(f"An error occurred when trying to check if a reservation was avaiable to be borrowed: {e}")
    ####
    # Deals with fulfilling a reservation when a reservation is borrowed by the user
    # - CLY 13-02-24 - 
    ####
    def isFulfilled (self, book_id, user_id):
        try:
            cursor = self.conn.cursor()
            # Get reservation Id
            cursor.execute("SELECT reservationID, userID from Reservations WHERE bookID = ? AND isFulfilled = 0 ORDER BY reservationDate DESC LIMIT 1", (book_id,))
            res = cursor.fetchone()
            if res:
                reservation_id, userID = res
                if userID == user_id:
                    cursor.execute("UPDATE Reservations SET isFulfilled = 1 WHERE reservationID = ?", (reservation_id,))
                    self.conn.commit()
                    print("Reservation have been fulfilled")
        except sqlite3.Error as e:
            print(f"An error occurred when trying to fulfill a reservation: {e}")
        
''''
# Example usage - Debug code lines for unit
if __name__ == "__main__":
    # Connect to SQLite database
    conn = Database.DatabaseConnection()
    #conn.connect()
    reservation_system = Reservation(conn.connect())

    # Example usage: Reserve a book
    reservation_system.reserve_book(1, 1)

    # Example usage: Fulfill a reservation
    reservation_system.isFulfilled(1, 1)

    # Example usage: Check reservation availability
    reservation_system.check_reservation_availbility(1)

    # Close the database connection
    conn.close()
'''