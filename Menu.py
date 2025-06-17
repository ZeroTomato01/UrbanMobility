import hashlib
from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate

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
    def service_engineer_menu(user: User):
        menu_options = [
        ("1", "Update own password"),
        ("2", "Search/retrieve scooter + update"),
        ("3", "Print profile info"),
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
                    # log update password event
                    update_password(user)
                case "2":
                    # log search/retrieve scooter info event + update
                    search_print_update_scooter(user)
                case "3":
                    print_profile(user)
                case _:
                    print("Invalid option. Please try again.")

    @staticmethod
    def system_admin_menu(user: User):
        menu_options = [
            ("1", "Update own password"),
            ("2", "Search/retrieve scooter + update"),
            ("3", "List users and roles"),
            ("4", "Add Service Engineer"),
            ("5", "Update Service Engineer profile"),
            ("6", "Delete Service Engineer"),
            ("7", "Reset Service Engineer password (temp password)"),
            ("8", "update own account"),
            ("9", "delete own account"),
            ("10", "Create backup"),
            ("11", "Restore backup (with restore-code from SA)"),
            ("12", "Print logs"),
            ("13", "Add Traveller"),
            ("14", "Update Traveller"),
            ("15", "Add Scooter"),
            ("16", "Update Scooter"),
            ("17", "Delete Scooter"),
            ("18", "Search/retrieve Traveller info"),
            ("0", "Logout"),
        ]
        while True:
            print("\n--- System Administrator Menu ---")
            for num, desc in menu_options:
                print(f"{num}. {desc}")
            choice = input("Select an option (number): ").strip()
            match choice:
                case "0":
                    # log the logout event
                    exit()
                case "1":
                    # log update password event
                    update_password(user)
                case "2":
                    # log search/retrieve scooter info event + update
                    search_print_update_scooter(user)
                case "3":
                    print("List users and roles selected.")
                case "4":
                    # log add service engineer event
                    add_service_engineer()
                case "5":
                    print("Update Service Engineer profile selected.")
                case "6":
                    print("Delete Service Engineer selected.")
                case "7":
                    print("Reset Service Engineer password (temp password) selected.")
                case "8":
                    print("Update own account selected.")
                case "9":
                    print("Delete own account selected.")
                case "10":
                    print("Create backup selected.")
                case "11":
                    print("Restore backup (with restore-code from SA) selected.")
                case "12":
                    print("Print logs selected.")
                case "13":
                    print("Add Traveller selected.")
                case "14":
                    print("Update Traveller selected.")
                case "15":
                    add_scooter()
                case "16":
                    print("Update Scooter selected.")
                case "17":
                    print("Delete Scooter selected.")
                case "18":
                    print("Search/retrieve Traveller info selected.")
                case _:
                    print("Invalid option. Please try again.")

    @staticmethod
    def super_admin_menu(user: User):
        menu_options = [
            ("1", "Update scooter attributes"),
            ("2", "Search/retrieve scooter info"),
            ("3", "List users and roles"),
            ("4", "Add Service Engineer"),
            ("5", "Update Service Engineer profile"),
            ("6", "Delete Service Engineer"),
            ("7", "Reset Service Engineer password (temp password)"),
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
            ("19", "Reset System Administrator password (temp password)"),
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
                    # log the add service engineer event
                    add_service_engineer()
                case "5":
                    print("Update Service Engineer profile selected.")
                case "6":
                    print("Delete Service Engineer selected.")
                case "7":
                    print("Reset Service Engineer password (temp password) selected.")
                case "8":
                    print("View logs selected.")
                case "9":
                    print("Add Traveller selected.")
                case "10":
                    print("Update Traveller selected.")
                case "11":
                    print("Delete Traveller selected.")
                case "12":
                    # log the add scooter event
                    add_scooter()
                case "13":
                    print("Update Scooter selected.")
                case "14":
                    print("Delete Scooter selected.")
                case "15":
                    print("Search/retrieve Traveller info selected.")
                case "16":
                    # log the add system administrator event
                    add_system_admin()
                case "17":
                    print("Update System Administrator profile selected.")
                case "18":
                    print("Delete System Administrator selected.")
                case "19":
                    print("Reset System Administrator password (temp password) selected.")
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

@staticmethod
def update_password(user: User):
    print("Update own password selected.")
    row_id = Utility.fetch_userinfo(user.username, row_id=True)
    new_password = Validate.validate_input("Enter new password: ", custom_validator=Utility.is_valid_password)
    Utility.update_passwordDB(new_password, row_id)

@staticmethod
def print_profile(user: User):
    print("Print profile info selected.")
    Utility.print_userinfo(user)

@staticmethod
def search_print_update_scooter(user: User):
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
            Utility.update_scooter_attributes(user, scooter)
        return

@staticmethod
def add_service_engineer():
    print("Add Service Engineer selected.")
    new_user = User(role="Service Engineer")
    new_user = Validate.Validate_user(new_user)
    Utility.Add_user(new_user)

@staticmethod
def add_system_admin():
    print("Add System Administrator selected.")
    new_user = User(role="System Administrator")
    new_user = Validate.Validate_user(new_user)
    Utility.Add_user(new_user)

@staticmethod
def add_scooter():
    print("Add Scooter selected.")
    new_scooter = Scooter()
    new_scooter = Validate.Validate_addscooter(new_scooter, add=True)
    Utility.Add_scooter(new_scooter)