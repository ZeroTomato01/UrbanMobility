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

