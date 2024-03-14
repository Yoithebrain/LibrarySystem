import sys
import StartMenu

def main():
    try:
        while True:
            print("1. Login")
            print("2. Create new user")
            print("3. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                StartMenu.login()
            elif choice == '2':
                StartMenu.create_user()
            elif choice == '3':
                print("Exiting program.")
                sys.exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    finally:
        # Close the database connection when the program exits
        StartMenu.close_database_connection()

if __name__ == "__main__":
    main()
