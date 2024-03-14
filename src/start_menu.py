import admin_menu
from user import user
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
                admin_menu.admin_menu()
            else:
                print("\nYou are not an admin.")
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
