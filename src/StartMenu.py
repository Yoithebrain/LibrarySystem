import AdminMenu
import UserMenu
from User import user
from Database import DatabaseConnection

db_connection = DatabaseConnection()

def login():
    username = input("\nEnter your username: ")
    password = input("\nEnter your password: ")
    
    user_data = user.load_user(username)
    if user_data:
        user_obj = user_data[1]
        if user_obj.verify_password(password):
            print("Login successful!")
            if user_obj.isAdmin:
                print("\nYou are logged in as admin")
                AdminMenu.admin_menu()
            else:
                print("\nYou are logged in as user")
                UserMenu.user_menu(userID=user_data[0])
        else:
            print("\nIncorrect password.")
    else:
        print("\nUser not found.")

def create_user():
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    new_user = user(name, address, username, password)
    user.save_user(new_user)
    print("User created successfully.\n")

def close_database_connection():
    db_connection.close()
