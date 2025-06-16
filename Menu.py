import hashlib
from Models.User import User
from Utils import Utility

class Menu:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def login():
        print("=== Urban Mobility Backend System ===")
        username = ''
        while True:
            if len(username) == 0:
                username = input("Username: ")
            password = input("Password: ")

            user = Utility.fetch_userinfo(username)
            if not user:
                print("Invalid username")
                # log the failed login attempt
                username = ''
                continue

            if user.password != hashlib.sha256(password.encode('utf-8')).hexdigest():
                print("Invalid password")
                # log the failed login attempt
                password = ''
                continue

            return user
        



    @staticmethod
    def service_engineer_menu():
        menu_options = [
        ("1", "Update own password"),
        ("2", "Update scooter attributes"),
        ("3", "Search/retrieve scooter info"),
        ("4", "Print profile info"),
        ("0", "Logout"),
        ]
        while True:
            print("\n--- Service Engineer Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()
            match choice:
                case "0":
                    # log the logout event
                    exit()
                case "1":
                    print("Update own password selected.")
                case "2":
                    print("Update scooter attributes selected.")
                case "3":
                    print("search/retrieve scooter info selected.")
                case _:
                    print("Invalid option. Please try again.")

    @staticmethod
    def system_admin_menu():
        while True:
            print("\n--- System Administrator Menu ---")
            print("1. Update own password")
            print("2. Update scooter attributes")
            print("3. Search/retrieve scooter info")
            print("4. List users and roles")
            print("5. Add Service Engineer")
            print("6. Update Service Engineer profile")
            print("7. Delete Service Engineer")
            print("8. Reset Service Engineer password")
            print("9. Update own profile")
            print("10. Delete own account")
            print("11. Backup system")
            print("12. Restore backup (with restore-code)")
            print("13. View logs")
            print("14. Add Traveller")
            print("15. Update Traveller")
            print("16. Delete Traveller")
            print("17. Add Scooter")
            print("18. Delete Scooter")
            print("19. Search/retrieve Traveller info")
            print("0. Logout")
            choice = input("Select an option: ")
            if choice == "0":
                break
            # TODO: Implement each option

    @staticmethod
    def super_admin_menu():
        menu_options = [
            ("1", "Update scooter attributes"),
            ("2", "Search/retrieve scooter info"),
            ("3", "List users and roles"),
            ("4", "Add Service Engineer"),
            ("5", "Update Service Engineer profile"),
            ("6", "Delete Service Engineer"),
            ("7", "Reset Service Engineer password"),
            ("8", "View logs"),
            ("9", "Add Traveller"),
            ("10", "Update Traveller"),
            ("11", "Delete Traveller"),
            ("12", "Add Scooter"),
            ("13", "Update Scooter"),
            ("14", "Delete Scooter"),
            ("15", "Search/retrieve Traveller info"),
            ("16", "Add System Administrator"),
            ("17", "Update System Administrator profile"),
            ("18", "Delete System Administrator"),
            ("19", "Reset System Administrator password"),
            ("20", "Backup system"),
            ("21", "Restore backup"),
            ("22", "Generate restore-code"),
            ("23", "Revoke restore-code"),
            ("0", "Logout"),
        ]

        while True:
            print("\n--- Super Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()

            match choice:
                case "0":
                    # log the logout event
                    exit()
                case "1":
                    print("Update scooter attributes selected.")
                case "2":
                    print("Search/retrieve scooter info selected.")
                case "3":
                    print("List users and roles selected.")
                case "4":
                    print("Add Service Engineer selected.")
                    user = User(role="Service Engineer")
                    user = Utility.Validate_service_engineer(user)
                    Utility.Add_user(user)
                case "5":
                    print("Update Service Engineer profile selected.")
                case "6":
                    print("Delete Service Engineer selected.")
                case "7":
                    print("Reset Service Engineer password selected.")
                case "8":
                    print("View logs selected.")
                case "9":
                    print("Add Traveller selected.")
                case "10":
                    print("Update Traveller selected.")
                case "11":
                    print("Delete Traveller selected.")
                case "12":
                    print("Add Scooter selected.")
                case "13":
                    print("Update Scooter selected.")
                case "14":
                    print("Delete Scooter selected.")
                case "15":
                    print("Search/retrieve Traveller info selected.")
                case "16":
                    print("Add System Administrator selected.")
                case "17":
                    print("Update System Administrator profile selected.")
                case "18":
                    print("Delete System Administrator selected.")
                case "19":
                    print("Reset System Administrator password selected.")
                case "20":
                    print("Backup system selected.")
                case "21":
                    print("Restore backup selected.")
                case "22":
                    print("Generate restore-code selected.")
                case "23":
                    print("Revoke restore-code selected.")
                case _:
                    print("Invalid option. Please try again.")
