import sqlite3
from Models.Traveller import Traveller
from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate
import os


class SystemAdminFunctions:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")

    @staticmethod
    def add_service_engineer(user: User):
        print("Add Service Engineer selected.")
        new_user = User(role="Service Engineer")
        new_user = Validate.Validate_user(user, new_user)
        Utility.Add_user(user, new_user)

    @staticmethod
    def list_users_and_roles(user):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM users")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
            print(f"- {decrypted_username}: {row['role']}")

    @staticmethod
    def delete_other_account(user: User):
        if user.role == "System Administrator":
            allowed_deletes = ["Service Engineer"]
        if user.role == "Super Administrator":
            allowed_deletes = ["Service Engineer", "System Administrator"]
        print("Delete account of other user selected")
        while True:
            keyword = input("Enter user info to search: ").strip()
            delete_user = Utility.fetch_searchuser(keyword)
            if not delete_user:
                print("No user found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            if not delete_user.role in allowed_deletes:
                print("not allowed to delete this user")
                Utility.log_activity(user.username, "Delete user from DB", "Not allowed to delete this user", 3)
                continue
            Utility.print_userinfo(delete_user)
            delete = input("Delete user? (Y/N)").lower()
            if delete == 'y':
                Utility.delete_user(user, delete_user)
            return
    
    @staticmethod
    def delete_own_account(user: User):
        print("Delete own account selected")
        while True:
            delete = input("Delete user? (Y/N)").lower()
            if delete == 'y':
                delete_user = user
                Utility.delete_user(user, delete_user)
                from um_members import main
                main()
            return

    @staticmethod
    def update_account_engineer(user: User):
        print("Update account of engineer selected")
        while True:
            keyword = input("Enter user info to search: ").strip()
            update_user = Utility.fetch_searchuser(keyword, role="Service Engineer")
            if not update_user:
                print("No user found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_userinfo(update_user)
            update = input("Update user? (Y/N)").lower()
            if update == 'y':
                Utility.update_account(user, update_user)
            return
    
    @staticmethod
    def update_account_sysadmin(user: User):
        print("Update account of system admin selected")
        while True:
            keyword = input("Enter user info to search: ").strip()
            update_user = Utility.fetch_searchuser(keyword, role="System Administrator")
            if not update_user:
                print("No user found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_userinfo(update_user)
            update = input("Update user? (Y/N)").lower()
            if update == 'y':
                Utility.update_account(user, update_user)
            return
    
    @staticmethod
    def update_own_account(user: User):
        print("Update account of engineer selected")
        while True:
            Utility.print_userinfo(user)
            update = input("Update user? (Y/N)").lower()
            if update == 'y':
                Utility.update_account(user, user)
            return
        
    @staticmethod
    def update_traveller(user: User):
        print("Update traveller selected")
        while True:
            keyword = input("Enter user info to search: ").strip()
            update_traveller = Utility.fetch_search_traveller(keyword) #returns found traveller, decrypted
            if not update_traveller:
                print("No user traveller with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_travelerinfo(update_traveller) #prints found traveller, decrypted, accurately
            update = input("Update traveller? (Y/N)").lower()
            if update == 'y':
                Utility.update_traveller(user, update_traveller) #traveller to update should be original encrypted traveller, not a re-encrypted decrypted one
            return

    @staticmethod
    def print_logs(user: User):
        print("Print logs selected.")
        Utility.print_logs(user)

    @staticmethod
    def add_scooter(user: User):
        print("Add Scooter selected.")
        new_scooter = Scooter()
        new_scooter = Validate.Validate_addscooter(user, new_scooter)
        Utility.Add_scooter(user, new_scooter)
    
    @staticmethod
    def search_print_update_scooteradmin(user: User):
        print("Print scooter info selected.")
        while True:
            keyword = input("Enter scooter info to search: ").strip()
            scooter = Utility.fetch_scooter_info(keyword)
            if not scooter:
                print("No scooter found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_scooterinfo(scooter)
            edit = input("Edit scooter attributes? (Y/N)").lower()
            if edit == 'y':
                Utility.update_scooter_attributes_admin(user, scooter)
            return
    
    @staticmethod
    def create_backup(user: User):
        print("create backup")
        Utility.create_backup(user)

    @staticmethod
    def delete_scooter(user: User):
        print("Delete scooter selected.")
        while True:
            keyword = input("Enter scooter info to search: ").strip()
            scooter = Utility.fetch_scooter_info(keyword)
            if not scooter:
                print("No scooter found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_scooterinfo(scooter)
            edit = input("Delete scooter? (Y/N)").lower()
            if edit == 'y':
                Utility.delete_scooterfromDB(user, scooter)
            return
        
    @staticmethod
    def add_traveller(user:User):
        print("Add Traveller selected.")
        new_traveller = Traveller()
        new_traveller = Validate.Validate_addtraveller(user, new_traveller)
        Utility.Add_traveller(user, new_traveller)

    @staticmethod
    def delete_traveller(user: User):
        print("Delete atraveller selected")
        while True:
            keyword = input("Enter traveller info to search: ").strip()
            delete_traveller = Utility.fetch_search_traveller(keyword)
            if not delete_traveller:
                print("No traveller found with that info.")
                end_search = input("end search? (Y/N)").lower()
                if end_search == 'y':
                    return
                continue
            Utility.print_travelerinfo(delete_traveller)
            delete = input("Delete traveller? (Y/N)").lower()
            if delete == 'y':
                Utility.delete_traveller(user, delete_traveller)

    @staticmethod
    def restore_backup(user: User):
        if user.role != "System Administrator":
            print("Access denied: only System Administrators can perform a restore.")
            return

        if not user.restore_code:
            print("No restore code found. Ask a Super Administrator to assign one first.")
            return

        try:
            # Translate restore_code to backup filename
            backup_filename = Utility.get_backup_filename_from_restore_code(user.restore_code)
            if not backup_filename:
                print("Invalid restore code or no matching backup found.")
                return

            backup_path = os.path.join("backups", backup_filename)

            print(f"\nYou are about to restore backup: {backup_filename}")
            confirm = input("Are you sure? This will overwrite current database files. Type 'yes' to confirm: ").strip().lower()

            if confirm != "yes":
                print("Restore cancelled. Returning to menu.")
                return

            # Perform the actual restore using the utility method you provided
            Utility.restore_backup(backup_path)
            Utility.revoke_backup_code(user, user)
            
            
            # Log the action
            Utility.log_activity(
                user.username,
                "Restored backup",
                additional_info=f"Restored backup from {backup_filename}",
                suspicious_count=0
            )

        except Exception as e:
            print(f"Restore failed: {e}")
            Utility.log_activity(
                user.username,
                "Restore failed",
                additional_info=str(e),
                suspicious_count=3
            )

    @staticmethod
    def assign_temp_password(admin_user: User):
        if admin_user.role not in ["System Administrator", "Super Administrator"]:
            print("Access denied: only System or Super Administrators can assign temp passwords.")
            return

        target_username = input("Enter the Service Engineer username to reset password for: ").strip()
        service_engineer = Utility.fetch_searchuser(target_username, role="Service Engineer")

        if not service_engineer:
            print(f"No Service Engineer user found matching '{target_username}'.")
            return

        temp_password = Utility.generate_temp_password()

        # Call the utility method to update temp_password in DB
        Utility.update_temp_password(admin_user, target_username, temp_password)
