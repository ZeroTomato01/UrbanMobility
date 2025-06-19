from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate


class SuperAdminFunctions:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")

    @staticmethod
    def add_system_admin(user: User):
        print("Add System Admin selected.")
        new_user = User(role="System Administrator")
        new_user = Validate.Validate_user(user, new_user)
        Utility.Add_user(user, new_user)

    
    @staticmethod
    def generate_restoreCode(user: User):
        if user.role != "Super Administrator":
            print("Access denied: only Super Administrators can generate restore codes.")
            return

        backup_filename = input("Enter the name of the backup file (e.g. backup_20250619_185832.zip): ").strip()

        restore_code = Utility.generate_backup_code(backup_filename, user)
        if not restore_code:
            print("Failed to generate restore code. Returning to menu.")
            return

        # Ask for the System Admin's username
        target_username = input("Enter the username of the System Administrator to assign the code to: ").strip()

        # Use fetch_searchuser
        target_user = Utility.fetch_searchuser(target_username, role="System Administrator")

        if not target_user:
            print(f"No System Administrator found with username '{target_username}'. Returning to menu.")
            return

        # Assign and update restore code
        Utility.update_backup_code(user, target_user, restore_code)

        print(f"Restore code '{restore_code}' assigned to '{target_username}'.")


    @staticmethod
    def revoke_backup_code(user: User):
        if user.role != "Super Administrator":
            print("Access denied: only Super Administrators can revoke restore codes.")
            return

        target_username = input("Enter the username of the System Administrator to revoke the restore code from: ").strip()

        target_user = Utility.fetch_searchuser(target_username, role="System Administrator")
        if not target_user:
            print(f"No System Administrator found with username '{target_username}'. Returning to menu.")
            return

        Utility.revoke_backup_code(user, target_user)

        
    @staticmethod
    def assign_temp_password(admin_user: User):
        if admin_user.role not in ["Super Administrator"]:
            print("Access denied: only Super Administrators can assign temp passwords.")
            return

        target_username = input("Enter the System Admin username to reset password for: ").strip()
        system_admin = Utility.fetch_searchuser(target_username, role="System Administrator")

        if not system_admin:
            print(f"No System Administrator user found matching '{target_username}'.")
            return

        temp_password = Utility.generate_temp_password()

        # Call the utility method to update temp_password in DB
        Utility.update_temp_password(admin_user, target_username, temp_password)