import sqlite3
from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate


class SystemAdminFunctions:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    # ("1", "Update own password"),
    # ("2", "Update scooter attributes"),
    # ("3", "Search/retrieve scooter info"),
    # ("4", "List users and roles"),
    # ("5", "Add Service Engineer"),
    # ("6", "Update Service Engineer profile"),
    # ("7", "Delete Service Engineer"),
    # ("8", "Reset Service Engineer password (temp password)"),
    # ("9", "update own account"),
    # ("10", "delete own account"),
    # ("11", "Create backup"),
    # ("12", "Restore backup (with restore-code from SA)"),
    # ("13", "Print logs"),
    # ("14", "Add Traveller"),
    # ("15", "Update Traveller"),
    # ("16", "Add Scooter"),
    # ("17", "Update Scooter"),
    # ("18", "Delete Scooter"),
    # ("19", "Search/retrieve Traveller info"),
    # ("0", "Logout"),


    @staticmethod
    def update_password(user: User):
        print("Update own password selected.")
        row_id = Utility.fetch_userinfo(user.username, row_id=True)
        new_password = Validate.validate_input("Enter new password: ",username=user.username, custom_validator=Validate.is_valid_password)
        Utility.update_passwordDB(user, new_password, row_id)

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
    def update_service_engineer_profile(user):
        return

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
    def reset_service_engineer_password(user):
        return

    @staticmethod
    def update_own_account(user):
        return

    @staticmethod
    def delete_own_account(user):
        return

    @staticmethod
    def create_backup(user):
        return

    @staticmethod
    def restore_backup(user):
        return

    @staticmethod
    def print_logs(user: User):
        print("Print logs selected.")
        Utility.print_logs(user)

    @staticmethod
    def add_traveller(user):
        return

    @staticmethod
    def update_traveller(user):
        return

    @staticmethod
    def add_scooter(user: User):
        print("Add Scooter selected.")
        new_scooter = Scooter()
        new_scooter = Validate.Validate_addscooter(user, new_scooter, add=True)
        Utility.Add_scooter(user, new_scooter)

    @staticmethod
    def update_scooter(user):
        return

    @staticmethod
    def delete_scooter(user):
        return

    @staticmethod
    def search_retrieve_traveller_info(user):
        return
        