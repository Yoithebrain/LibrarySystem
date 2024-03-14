import sqlite3
import logging
from datetime import datetime
from Database import DatabaseConnection

class Book:
    def __init__(self, bookID, title, author, publicationYear, genre, description, creationDate, updatedDate):
        self.bookID = bookID
        self.title = title
        self.author = author
        self.publicationYear = publicationYear
        self.genre = genre
        self.description = description
        self.creationDate = creationDate if creationDate else datetime.now()
        self.updatedDate = updatedDate if updatedDate else datetime.now()
    
    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Publication Date: {self.publication_date}, Genre: {self.genre}, Description: {self.description}, Creation Date: {self.creation_date}, Updated Date: {self.updated_date}"

    @classmethod
    def load_book_on_ID(cls, book_id):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Books WHERE bookID=?", (book_id,))
            book_data = cursor.fetchone()

            if book_data:
                return cls(*book_data)
            else:
                return None
        except sqlite3.Error as e:
            logging.error("Error occurred while loading book {}: {}".format(book_id, e))
            return None
        finally:
            cursor.close()

    @classmethod
    def get_all_books(cls):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Books")
            books_data = cursor.fetchall()

            books = []
            for book_data in books_data:
                books.append(cls(*book_data))
        
            return books
        except sqlite3.Error as e:
            logging.error("Error occurred while retrieving all books: {}".format(e))
            return []
        finally:
            cursor.close()

    @classmethod
    def get_all_bookIDs(cls):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            cursor.execute("SELECT bookID FROM Books")
            book_ids = [row[0] for row in cursor.fetchall()]
            
            return book_ids
        except sqlite3.Error as e:
            logging.error("Error occurred while retrieving book IDs: {}".format(e))
            return []
        finally:
            cursor.close()

    #Get all available books using a list of ids
    @classmethod
    def get_available_books(cls, unavailableIDs):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            if not unavailableIDs:
                cursor.execute("SELECT * FROM Books")
            else:
                placeholder = ",".join(["?" for _ in range(len(unavailableIDs))])
                query = f"SELECT * FROM Books WHERE bookID NOT IN ({placeholder})"
                cursor.execute(query, unavailableIDs)

            books_data = cursor.fetchall()

            books = []
            for book_data in books_data:
                books.append(cls(*book_data))
        
            return books
        except sqlite3.Error as e:
            logging.error("Error occurred while retrieving available books: {}".format(e))
            return []
        finally:
            cursor.close()

    @classmethod
    def get_books_by_ids(cls, book_ids):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            if not book_ids:
                return []

            placeholder = ",".join(["?" for _ in range(len(book_ids))])
            query = f"SELECT * FROM Books WHERE bookID IN ({placeholder})"
            cursor.execute(query, book_ids)

            books_data = cursor.fetchall()

            books = []
            for book_data in books_data:
                books.append(cls(*book_data))
        
            return books
        except sqlite3.Error as e:
            logging.error("Error occurred while retrieving books by IDs: {}".format(e))
            return []
        finally:
            cursor.close()