import hashlib
from Models.User import User
from Utils import Utility
from system_admin_functions import SystemAdminFunctions
from super_admin_functions import SuperAdminFunctions
from service_engineer_functions import ServiceEngineerFunctions
import sqlite3
from Validate import Validate

class Menu:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def login():
        print("=== Urban Mobility Backend System ===")
        username = ''
        suspicious_count = 0
        encrypt = Utility.load_key()

        while True:
            if len(username) == 0:
                username = input("Username: ").strip()

            user = Utility.fetch_userinfo(username)
            if not user:
                print("Invalid username")
                suspicious_count += 1
                Utility.log_activity('', "Login attempt", f"Invalid username: \"{username}\" was used", suspicious_count)
                username = ''
                continue

            if user.role in ["Service Engineer", "System Administrator"] and user.temp_password:
                # Ask for temp password first
                print(f"Temporary password required for login: \"{user.temp_password}\"")
                entered_temp_pass = input("Enter temporary password: ").strip()

                # user.temp_password is already decrypted, so no need to decrypt again
                if entered_temp_pass != user.temp_password:
                    print("Incorrect temporary password")
                    suspicious_count += 1
                    Utility.log_activity(username, "Temp password attempt", "Incorrect temp password entered", suspicious_count)
                    continue

                print("Temporary password accepted. Please create a new password.")

                while True:
                    new_password = input("New password: ").strip()
                    if not Validate.is_valid_password(new_password):
                        print("Password does not meet complexity requirements. Try again.")
                        continue

                    confirm_password = input("Confirm new password: ").strip()
                    if new_password != confirm_password:
                        print("Passwords do not match. Try again.")
                        continue

                    # Update the user's password in the database
                    row_id = Utility.fetch_userinfo(user.username, row_id=True)
                    Utility.update_passwordDB(user, new_password, row_id)
                    Utility.update_temp_password(user, user.username, None)  # Clear temp password

                    print("Password updated successfully. Logging in...")
                    Utility.log_activity(username, "Password reset via temp password", "Password reset successful", 0)
                    suspicious_count = 0
                    return user

            # Normal password login flow
            password = input("Password: ")
            if user.password != hashlib.sha256(password.encode('utf-8')).hexdigest():
                print("Invalid password")
                suspicious_count += 1
                Utility.log_activity(username, "Login attempt", f"Invalid password with username: \"{username}\" was used", suspicious_count)
                continue

            suspicious_count = 0  # Reset suspicious count on successful login
            Utility.log_activity(username, "Login successful", "", suspicious_count)
            return user


        



    @staticmethod
    def service_engineer_menu(user: User):
        menu_options = [
        ("1", "Update own password"),
        ("2", "Search/retrieve scooter + update"),
        ("3", "Print profile info"),
        ("0", "Logout"),
        ]
        suspicious_count = 0
        while True:
            print("\n--- Service Engineer Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()
            match choice:
                case "0":
                    Utility.log_activity(user.username, "Logout succesful", "")
                    exit()
                case "1":
                    ServiceEngineerFunctions.update_password(user)
                case "2":
                    ServiceEngineerFunctions.search_print_update_scooterengineer(user)
                case "3":
                    ServiceEngineerFunctions.print_profile(user)
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

    @staticmethod
    def system_admin_menu(user: User):
        menu_options = [
            ("1", "Update own password"), #1 Users
            ("2", "Search/retrieve scooter + update"), #2 Scooter
            ("3", "Print profile info"),  #Users
            ("4", "List users and roles"), #Users
            ("5", "Add Service Engineer"), #Users
            ("6", "Update Service Engineer profile"), #Users
            ("7", "Delete Service Engineer"), #Users
            ("8", "Reset Service Engineer password (temp password)"), #Users
            ("9", "update own account"), #Users
            ("10", "delete own account"), #Users
            ("11", "Create backup"), #3 Backup
            ("12", "Restore backup (with restore-code from SA)"), #Backup
            ("13", "Print logs"), #4 Logs
            ("14", "Add Traveller"), #5 Traveller
            ("15", "Delete Traveller"), #Traveller
            ("16", "Add Scooter"), #Scooter
            ("17", "Delete Scooter"), #Scooter
            ("18", "Search/retrieve Traveller info + update"), #Traveller
            ("0", "Logout"), #6 Logout
        ]
        suspicious_count = 0
        while True:
            print("\n--- System Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()
            match choice:
                case "0":
                    Utility.log_activity(user.username, "Logout succesful", "")
                    exit()
                case "1":
                    ServiceEngineerFunctions.update_password(user)
                case "2":
                    SystemAdminFunctions.search_print_update_scooteradmin(user)
                case "3":
                    ServiceEngineerFunctions.print_profile(user)
                case "4":
                    SystemAdminFunctions.list_users_and_roles(user)
                case "5":
                    SystemAdminFunctions.add_service_engineer(user)
                case "6":
                    SystemAdminFunctions.update_account_engineer(user)
                case "7":
                    SystemAdminFunctions.delete_other_account(user)
                case "8":
                    SystemAdminFunctions.assign_temp_password(user)
                case "9":
                    SystemAdminFunctions.update_own_account(user)
                case "10":
                    SystemAdminFunctions.delete_own_account(user)
                case "11":
                    SystemAdminFunctions.create_backup(user)
                case "12":
                    SystemAdminFunctions.restore_backup(user)
                case "13":
                    SystemAdminFunctions.print_logs(user)
                case "14":
                    SystemAdminFunctions.add_traveller(user)
                case "15":
                    SystemAdminFunctions.delete_traveller(user)
                case "16":
                    SystemAdminFunctions.add_scooter(user)
                case "17":
                    SystemAdminFunctions.delete_scooter(user)
                case "18":
                    SystemAdminFunctions.update_traveller(user)
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

    @staticmethod
    def super_admin_menu(user: User):
        menu_options = [
            ("1", "Search/retrieve scooter info + update"), #Scooter
            ("2", "List users and roles"), #Users
            ("3", "Add Service Engineer"), #Users
            ("4", "Update Service Engineer profile"), #Users
            ("5", "Delete other user (Engineer or sys admin)"), #Users
            ("6", "Reset Service Engineer password (temp password)"), #Users
            ("7", "View logs"), #Logs
            ("8", "Add Traveller"), #Travellers
            ("9", "Delete Traveller"), #Travellers
            ("10", "Add Scooter"), #Scooters
            ("11", "Delete Scooter"), #Scooters
            ("12", "Search/retrieve Traveller info + update"), #Travellers
            ("13", "Add System Administrator"), #Users
            ("14", "Update System Administrator profile"), #Users
            ("15", "Reset System Administrator password (temp password)"), #Users
            ("16", "Backup system"), #Backup, super_admin moet deze toch niet kunnen?
            ("17", "Restore backup"), #Backup
            ("18", "Generate restore-code"), #Backup
            ("19", "Revoke restore-code"), #Backup
            ("0", "Logout"), #Logout
        ]

        suspicious_count = 0
        while True:
            print("\n--- Super Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()

            match choice:
                case "0":
                    Utility.log_activity(user.username, "Logout succesful")
                    exit()
                case "1":
                    SystemAdminFunctions.search_print_update_scooteradmin(user)
                case "2":
                    SystemAdminFunctions.list_users_and_roles(user)
                case "3":
                    SystemAdminFunctions.add_service_engineer(user)
                case "4":
                    SystemAdminFunctions.update_account_engineer(user)
                case "5":
                    SystemAdminFunctions.delete_other_account(user)
                case "6":
                    SystemAdminFunctions.assign_temp_password(user)
                case "7":
                    SystemAdminFunctions.print_logs(user)
                case "8":
                    SystemAdminFunctions.add_traveller(user)
                case "9":
                    SystemAdminFunctions.delete_traveller(user)
                case "10":
                    SystemAdminFunctions.add_scooter(user)
                case "11":
                    SystemAdminFunctions.delete_scooter(user)
                case "12":
                    SystemAdminFunctions.update_traveller(user)
                case "13":
                    SuperAdminFunctions.add_system_admin(user)
                case "14":
                    SystemAdminFunctions.update_account_sysadmin(user)
                case "15":
                    SuperAdminFunctions.assign_temp_password(user)
                case "16":
                    SystemAdminFunctions.create_backup(user)
                case "17":
                    SuperAdminFunctions.restore_backup_from_menu(user)
                case "18":
                    SuperAdminFunctions.generate_restoreCode(user)
                case "19":
                    SuperAdminFunctions.revoke_backup_code(user)
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)