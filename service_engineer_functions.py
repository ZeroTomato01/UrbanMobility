from Models.User import User
from Models.Scooter import Scooter
from Utils import Utility
from Validate import Validate


class ServiceEngineerFunctions:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def update_password(user: User):
        print("Update own password selected.")
        row_id = Utility.fetch_userinfo(user.username, row_id=True)
        new_password = Validate.validate_input("Enter new password: ", username=user.username, custom_validator=Validate.is_valid_password)
        Utility.update_passwordDB(user, new_password, row_id)

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