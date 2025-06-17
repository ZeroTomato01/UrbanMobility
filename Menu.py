import hashlib
from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate
from system_admin_functions import SystemAdminFunctions
from super_admin_functions import SuperAdminFunctions
from service_engineer_functions import ServiceEngineerFunctions

class Menu:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def login():
        print("=== Urban Mobility Backend System ===")
        username = ''
        suspicious_count = 0
        while True:
            if len(username) == 0:
                username = input("Username: ")
            password = input("Password: ")

            user = Utility.fetch_userinfo(username)
            if not user:
                print("Invalid username")
                suspicious_count += 1
                Utility.log_activity('', "Login attempt", f"Invalid username: \"{username}\" was used", suspicious_count)
                username = ''
                continue

            if user.password != hashlib.sha256(password.encode('utf-8')).hexdigest():
                print("Invalid password")
                suspicious_count += 1
                Utility.log_activity(username, "Login attempt", f"Invalid password with username: \"{username}\" was used", suspicious_count)
                password = ''
                continue
            
            suspicious_count = 0  # Reset suspicious count on successful login
            Utility.log_activity(username, "Login succesful", "", suspicious_count)
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
                    ServiceEngineerFunctions.search_print_update_scooter(user)
                case "3":
                    ServiceEngineerFunctions.print_profile(user)
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

    @staticmethod
    def system_admin_menu(user: User):
        menu_options = [
            ("1", "Update own password"),
            ("2", "Search/retrieve scooter + update"),
            ("3", "Print profile info"),
            ("4", "List users and roles"),
            ("5", "Add Service Engineer"),
            ("6", "Update Service Engineer profile"),
            ("7", "Delete Service Engineer"),
            ("8", "Reset Service Engineer password (temp password)"),
            ("9", "update own account"),
            ("10", "delete own account"),
            ("11", "Create backup"),
            ("12", "Restore backup (with restore-code from SA)"),
            ("13", "Print logs"),
            ("14", "Add Traveller"),
            ("15", "Update Traveller"),
            ("16", "Add Scooter"),
            ("17", "Update Scooter"),
            ("18", "Delete Scooter"),
            ("19", "Search/retrieve Traveller info"),
            ("0", "Logout"),
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
                    ServiceEngineerFunctions.search_print_update_scooter(user)
                case "3":
                    ServiceEngineerFunctions.print_profile(user)
                case "4":
                    SystemAdminFunctions.list_users_and_roles(user)
                case "5":
                    SystemAdminFunctions.add_service_engineer(user)
                case "6":
                    SystemAdminFunctions.update_service_engineer_profile(user)
                case "7":
                    SystemAdminFunctions.delete_service_engineer(user)
                case "8":
                    SystemAdminFunctions.reset_service_engineer_password(user)
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
                    SystemAdminFunctions.update_traveller(user)
                case "16":
                    SystemAdminFunctions.add_scooter(user)
                case "17":
                    SystemAdminFunctions.update_scooter(user)
                case "18":
                    SystemAdminFunctions.delete_scooter(user)
                case "19":
                    SystemAdminFunctions.search_retrieve_traveller_info(user)
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)

    @staticmethod
    def super_admin_menu(user: User):
        menu_options = [
            ("1", "Search/retrieve scooter info + update"),
            ("2", "List users and roles"),
            ("3", "Add Service Engineer"),
            ("4", "Update Service Engineer profile"),
            ("5", "Delete Service Engineer"),
            ("6", "Reset Service Engineer password (temp password)"),
            ("7", "View logs"),
            ("8", "Add Traveller"),
            ("9", "Update Traveller"),
            ("10", "Delete Traveller"),
            ("11", "Add Scooter"),
            ("12", "Delete Scooter"),
            ("13", "Search/retrieve Traveller info"),
            ("14", "Add System Administrator"),
            ("15", "Update System Administrator profile"),
            ("16", "Delete System Administrator"),
            ("17", "Reset System Administrator password (temp password)"),
            ("18", "Backup system"),
            ("19", "Restore backup"),
            ("20", "Generate restore-code"),
            ("21", "Revoke restore-code"),
            ("0", "Logout"),
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
                    ServiceEngineerFunctions.search_print_update_scooter(user)
                case "2":
                    SystemAdminFunctions.list_users_and_roles(user)
                case "3":
                    SystemAdminFunctions.add_service_engineer(user)
                case "4":
                    print("Update Service Engineer profile selected.")
                case "5":
                    print("Delete Service Engineer selected.")
                case "6":
                    print("Reset Service Engineer password (temp password) selected.")
                case "7":
                    SystemAdminFunctions.print_logs(user)
                case "8":
                    print("Add Traveller selected.")
                case "9":
                    print("Update Traveller selected.")
                case "10":
                    print("Delete Traveller selected.")
                case "11":
                    SystemAdminFunctions.add_scooter(user)
                case "12":
                    print("Delete Scooter selected.")
                case "13":
                    print("Search/retrieve Traveller info selected.")
                case "14":
                    SuperAdminFunctions.add_system_admin(user)
                case "15":
                    print("Update System Administrator profile selected.")
                case "16":
                    print("Delete System Administrator selected.")
                case "17":
                    print("Reset System Administrator password (temp password) selected.")
                case "18":
                    print("Backup system selected.")
                case "19":
                    print("Restore backup selected.")
                case "20":
                    print("Generate restore-code selected.")
                case "21":
                    print("Revoke restore-code selected.")
                case _:
                    print("Invalid option. Please try again.")
                    suspicious_count += 1
                    Utility.log_activity(user.username, "Invalid option selected", f"Invalid option: {choice}", suspicious_count)