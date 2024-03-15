import logging
from BorrowSystem import BorrowSystem
from Book import Book

logging.basicConfig(level=logging.INFO)

class UserMenu:
    def __init__(self, user_id):
        self.user_id = user_id
        self.borrow_system = BorrowSystem()
    
    def borrow_book(self):
        try:
            unavailable_books = self.borrow_system.get_unavailable_books()  # Fetch unavailable books
            available_books = Book.get_available_books(unavailable_books)  # Fetch available books
            if available_books:
                for book in available_books:
                    print(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")
                
                book_id = input("Enter the ID of the book you want to borrow: ")
                self.borrow_system.borrow_book(self.user_id, book_id)
                logging.info("Book borrowed successfully!")
            else:
                logging.info("No available books found.")
        except Exception as e:
            logging.error("An error occurred during borrowing book:", e)

    def borrowed_books_list(self):
            try:
                borrowed_books_id = self.borrow_system.get_borrowed_book_ids(self.user_id)
                borrowed_books = Book.get_books_by_ids(borrowed_books_id) 
                if borrowed_books:
                    logging.info("Borrowed Books:")
                    for book in borrowed_books:
                        logging.info(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")
                else:
                    print("\n")
            except Exception as e:
                logging.error("An error occurred while displaying borrowed books:", e)

    def return_book(self):
        try:
            borrowed_books_id = self.borrow_system.get_borrowed_book_ids(self.user_id)
            borrowed_books = Book.get_books_by_ids(borrowed_books_id)
            if not borrowed_books:
                logging.info("No books borrowed.")
                return
            
            logging.info("Borrowed Books:")
            for book in borrowed_books:
                logging.info(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")

            borrow_id = input("Enter the ID of the borrowed book you want to return: ")
            valid_borrow_ids = [book.bookID for book in borrowed_books]
            
            try:
                borrow_id = int(borrow_id)  # Convert borrow_id to integer
            except ValueError:
                logging.info("Invalid book ID. Please enter a valid ID.")
                return
            
            if borrow_id not in valid_borrow_ids:
                logging.info("Invalid book ID. Please enter a valid ID.")
                return
            
            self.borrow_system.return_book(self.user_id, borrow_id)
            #logging.info("Book returned successfully!")
        except Exception as e:
            logging.error("An error occurred during returning book:", e)

    @classmethod
    def available_books(cls): 
        try:
            unavailable_books = BorrowSystem.get_unavailable_books()
            available_books = Book.get_available_books(unavailable_books)
            if available_books:
                for book in available_books:
                    logging.info(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")
            else:
                logging.info("No available books found.")
        except Exception as e:
            logging.error("An error occurred while displaying available books:", e)

    @classmethod
    def books_to_return(cls, userID):
        try:
            borrowed_books = BorrowSystem.return_all_books(userID)
            list_return = Book.get_books_by_ids(borrowed_books)
            if borrowed_books:
                for book in list_return:
                    print(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Borrow Date: {book.borrow_date}, Return Date: {book.return_date}")
            else:
                logging.info("No borrowed books available for return.")
        except Exception as e:
            logging.error("An error occurred while displaying borrowed books available for return:", e)

def user_menu(userID):
    while True:
        options = UserMenu(user_id=userID)
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. List Borrowed Books")
        print("4. Exit User Menu")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            options.borrow_book()
        elif choice == '2':
            options.return_book()
        elif choice == '3':
            options.borrowed_books_list() 
        elif choice == '4':
            logging.info("Exiting User Menu.")
            break
        else:
            logging.info("Invalid choice. Please enter a valid option.")
