import sys
import start_menu

def main():
    while True:
        print("1. Login")
        print("2. Create new user")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            start_menu.login()
        elif choice == '2':
            start_menu.create_user()
        elif choice == '3':
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()