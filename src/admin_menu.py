from user import user

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Update user")
        print("2. Delete user")
        print("3. Get all users")
        print("4. Logout")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            username = input("Enter the username of the user to update: ")
            user_data = user.load_user(username)
            if user_data:
                user_id, user_to_update = user_data
                print("User information:")
                print("Name:", user_to_update.name)
                print("Address:", user_to_update.address)
                print("Username:", user_to_update.username)
                print("Is Admin:", "Yes" if user_to_update.isAdmin else "No")
                print("Creation Date:", user_to_update.creationDate)
                print("Last Updated:", user_to_update.lastUpdated)
                
                print("\nUpdate options:")
                print("1. Update name")
                print("2. Update address")
                print("3. Update username")
                print("4. Update password")
                print("5. Toggle admin status")
                print("6. Cancel")
                update_choice = input("Enter your update choice: ")
                
                if update_choice == '1':
                    new_name = input("Enter the new name: ")
                    user_to_update.name = new_name
                elif update_choice == '2':
                    new_address = input("Enter the new address: ")
                    user_to_update.address = new_address
                elif update_choice == '3':
                    new_username = input("Enter the new username: ")
                    user_to_update.username = new_username
                elif update_choice == '4':
                    new_password = input("Enter the new password: ")
                    user_to_update.password = new_password
                elif update_choice == '5':
                    user_to_update.isAdmin = not user_to_update.isAdmin
                elif update_choice == '6':
                    print("Update canceled.")
                    continue
                
                print("\nUpdated user information:")
                print("Name:", user_to_update.name)
                print("Address:", user_to_update.address)
                print("Username:", user_to_update.username)
                print("Is Admin:", "Yes" if user_to_update.isAdmin else "No")
                print("Creation Date:", user_to_update.creationDate)
                print("Last Updated:", user_to_update.lastUpdated)
                
                confirm_update = input("Are you sure you want to update the user? (yes/no): ")
                if confirm_update.lower() in ['yes', 'y']:
                    updated_user = user.update_user(username, user_to_update)
                    if updated_user:
                        print("User updated successfully.")
                    else:
                        print("Failed to update user.")
                else:
                    print("Update canceled.")
            else:
                print("User not found.")
        elif choice == '2':
            username = input("Enter the username of the user to delete: ")
            confirm_delete = input(f"Are you sure you want to delete the user {username}? (yes/no): ")
            if confirm_delete.lower() in ['yes', 'y']:
                user.delete_user(username)
                print("User deleted successfully.")
            else:
                print("Deletion canceled.")
        elif choice == '3':
            all_users = user.get_all_users()
            for user_data in all_users:
                print(user_data)  # Display all users
        elif choice == '4':
            print("Logging out...\n")
            break
        else:
            print("Invalid choice.")
