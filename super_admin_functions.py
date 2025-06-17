from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate


class SuperAdminFunctions:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    

# ("1", "Update scooter attributes"),
# ("2", "Search/retrieve scooter info"),
# ("3", "List users and roles"),
# ("4", "Add Service Engineer"),
# ("5", "Update Service Engineer profile"),
# ("6", "Delete Service Engineer"),
# ("7", "Reset Service Engineer password (temp password)"),
# ("8", "View logs"),
# ("9", "Add Traveller"),
# ("10", "Update Traveller"),
# ("11", "Delete Traveller"),
# ("12", "Add Scooter"),
# ("13", "Update Scooter"),
# ("14", "Delete Scooter"),
# ("15", "Search/retrieve Traveller info"),
# ("16", "Add System Administrator"),
# ("17", "Update System Administrator profile"),
# ("18", "Delete System Administrator"),
# ("19", "Reset System Administrator password (temp password)"),
# ("20", "Backup system"),
# ("21", "Restore backup"),
# ("22", "Generate restore-code"),
# ("23", "Revoke restore-code"),
# ("0", "Logout"),

    @staticmethod
    def add_system_admin():
        print("Add System Admin selected.")
        new_user = User(role="System Administrator")
        new_user = Validate.Validate_user(new_user)
        Utility.Add_user(new_user)  