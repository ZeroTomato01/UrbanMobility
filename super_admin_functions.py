from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate
import os


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



    @staticmethod
    def restore_backup_from_menu(admin_user: User):
        if admin_user.role != "Super Administrator":
            print("Access denied: only Super Administrators can restore backups.")
            return

        backup_dir = "backups"
        if not os.path.isdir(backup_dir):
            print("No backup directory found.")
            return

        backups = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
        if not backups:
            print("No backups found in the /backups folder.")
            return

        print("=== Available Backups ===")
        for idx, backup_name in enumerate(backups, start=1):
            print(f"{idx}. {backup_name}")

        try:
            choice = int(input("Enter the number of the backup to restore: ").strip())
            if choice < 1 or choice > len(backups):
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        selected_backup = backups[choice - 1]
        backup_path = os.path.join(backup_dir, selected_backup)

        # Restore the selected backup
        try:
            Utility.restore_backup(backup_path)
            print(f"Backup '{selected_backup}' has been successfully restored.")
            Utility.log_activity(
                admin_user.username,
                "Restore backup",
                additional_info=f"Restored backup: {selected_backup}",
                suspicious_count=0
            )
        except Exception as e:
            print(f"Failed to restore backup: {e}")
            Utility.log_activity(
                admin_user.username,
                "Restore backup failed",
                additional_info=str(e),
                suspicious_count=3
            )
