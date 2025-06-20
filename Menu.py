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
            ("1", "Manage Users"),
            ("2", "Manage Travellers"),
            ("3", "Manage Scooters"),
            ("4", "Manage Backups"),
            ("5", "View Logs"),
            ("0", "Logout")
        ]

        user_menu_options = [
            ("1", "Update own password"), #1 Users
            ("2", "Print profile info"),  #Users
            ("3", "List users and roles"), #Users
            ("4", "Add Service Engineer"), #Users
            ("5", "Update Service Engineer profile"), #Users
            ("6", "Delete Service Engineer"), #Users
            ("7", "Reset Service Engineer password (temp password)"), #Users
            ("8", "update own account"), #Users
            ("9", "delete own account"), #Users
            ("0", "Back")
        ]

        traveller_menu_options = [
            ("1", "Add Traveller"), #Travellers
            ("2", "Delete Traveller"), #Travellers
            ("3", "Search/retrieve Traveller info + update"), #Travellers
            ("0", "Back")
        ]

        scooter_menu_options = [
            ("1", "Add Scooter"), #Scooters
            ("2", "Delete Scooter"), #Scooters
            ("3", "Search/retrieve scooter + update"), #2 Scooter
            ("0", "Back")
        ]

        backup_options = [
            ("1", "Create backup"), #3 Backup
            ("2", "Restore backup (with restore-code from SA)"), #Backup
            ("0", "Back")
        ]



        suspicious_count = 0
        while True:
            print("\n--- System Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()


            match choice:
                case "1":
                    while True:
                        print("\n--- Manage Users---")
                        for num, desc in user_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                ServiceEngineerFunctions.update_password(user)
                            case "2":
                                ServiceEngineerFunctions.print_profile(user)
                            case "3":
                                SystemAdminFunctions.list_users_and_roles(user)
                            case "4":
                                SystemAdminFunctions.add_service_engineer(user)
                            case "5":
                                SystemAdminFunctions.update_account_engineer(user)
                            case "6":
                                SystemAdminFunctions.delete_other_account(user)
                            case "7":
                                SystemAdminFunctions.assign_temp_password(user)
                            case "8":
                                SystemAdminFunctions.update_own_account(user)
                            case "9":
                                SystemAdminFunctions.delete_own_account(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)
                case "2": # Manage Travellers
                    while True:
                        print("\n--- Manage Travellers ---")
                        for num, desc in traveller_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.add_traveller(user)
                            case "2":
                                SystemAdminFunctions.delete_traveller(user)
                            case "3":
                                SystemAdminFunctions.update_traveller
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)
                            

                case "3": # Manage Scooter
                    while True:
                        print("\n--- Manage Scooters ---")
                        for num, desc in scooter_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.add_scooter(user)
                            case "2":
                                SystemAdminFunctions.delete_scooter(user)
                            case "3":
                                SystemAdminFunctions.search_print_update_scooteradmin(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

                case "4": # Manage Backups
                    while True:
                        print("\n--- Manage Backups ---")
                        for num, desc in backup_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.create_backup(user)
                            case "2":
                                SystemAdminFunctions.restore_backup(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

                case "5": # View logs
                    SystemAdminFunctions.print_logs(user)

                case "0": # Logout
                    Utility.log_activity(user.username, "Logout succesful")
                    exit()

                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

    @staticmethod
    def super_admin_menu(user: User):
        menu_options = [
            ("1", "Manage Users"),
            ("2", "Manage Travellers"),
            ("3", "Manage Scooters"),
            ("4", "Manage Backups"),
            ("5", "View Logs"),
            ("0", "Logout")
        ]

        user_menu_options = [
            ("1", "List users and roles"), #Users
            ("2", "Add Service Engineer"), #Users
            ("3", "Update Service Engineer profile"), #Users
            ("4", "Delete other user (Engineer or sys admin)"), #Users
            ("5", "Reset Service Engineer password (temp password)"), #Users
            ("6", "Add System Administrator"), #Users
            ("7", "Update System Administrator profile"), #Users
            ("8", "Reset System Administrator password (temp password)"), #Users
            ("0", "Back")
        ]

        traveller_menu_options = [
            ("1", "Add Traveller"), #Travellers
            ("2", "Delete Traveller"), #Travellers
            ("3", "Search/retrieve Traveller info + update"), #Travellers
            ("0", "Back")
        ]

        scooter_menu_options = [
            ("1", "Add Scooter"), #Scooters
            ("2", "Delete Scooter"), #Scooters
            ("0", "Back")
        ]

        backup_options = [
            ("1", "Backup system"), #Backup, super_admin moet deze toch niet kunnen?
            ("2", "Restore backup"), #Backup
            ("3", "Generate restore-code"), #Backup
            ("4", "Revoke restore-code"), #Backup
            ("0", "Back")
        ]

        suspicious_count = 0
        while True:
            print("\n--- Super Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()

            match choice:
                case "1":
                    while True:
                        print("\n--- Manage Users---")
                        for num, desc in user_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1": #Manage Users
                                SystemAdminFunctions.list_users_and_roles(user)
                            case "2":
                                SystemAdminFunctions.add_service_engineer(user)
                            case "3":
                                SystemAdminFunctions.update_account_engineer(user)
                            case "4":
                                SystemAdminFunctions.delete_other_account(user)
                            case "5":
                                SystemAdminFunctions.assign_temp_password(user)
                            case "6":
                                SuperAdminFunctions.add_system_admin(user)
                            case "7":
                                SystemAdminFunctions.update_account_sysadmin(user)
                            case "8":
                                SuperAdminFunctions.assign_temp_password(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)
                case "2": # Manage Travellers
                    while True:
                        print("\n--- Manage Travellers ---")
                        for num, desc in traveller_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.add_traveller(user)
                            case "2":
                                SystemAdminFunctions.delete_traveller(user)
                            case "3":
                                SystemAdminFunctions.update_traveller(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)
                            

                case "3": # Manage Scooter
                    while True:
                        print("\n--- Manage Scooters ---")
                        for num, desc in scooter_menu_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.add_scooter(user)
                            case "2":
                                SystemAdminFunctions.delete_scooter(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

                case "4": # Manage Backups
                    while True:
                        print("\n--- Manage Backups ---")
                        for num, desc in backup_options:
                            print(f"{num}. {desc}")
                        choice2 = input("Select an option (number): ").strip()
                        match choice2:
                            case "1":
                                SystemAdminFunctions.create_backup(user)
                            case "2":
                                SuperAdminFunctions.restore_backup_from_menu(user)
                            case "3":
                                SuperAdminFunctions.generate_restoreCode(user)
                            case "4":
                                SuperAdminFunctions.revoke_backup_code(user)
                            case "0": break
                            case _:
                                print("Invalid option. Please try again.")
                                suspicious_count += 1
                                Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

                case "5": # View logs
                    SystemAdminFunctions.print_logs(user)

                case "0": # Logout
                    Utility.log_activity(user.username, "Logout succesful")
                    exit()

                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)
