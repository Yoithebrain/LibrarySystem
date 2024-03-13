import sys
from user import user

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    user_obj = user.load_user(username)
    if user_obj:
        print("found user:", user_obj.username, "password: ", user_obj.password)
        if user.verify_password(user_obj, password):
            print("Login successful!")
            if user_obj.isAdmin:
                print("You are an admin.")
            else:
                print("You are not an admin.")
        else:
            print("Incorrect password.")
    else:
        print("User not found.")

def create_user():
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    new_user = user(name, address, username, password)
    user.save_user(new_user)
    print("User created successfully.")


#Test main for login
def main():
    while True:
        print("1. Login")
        print("2. Create new user")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            create_user()
        elif choice == '3':
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
