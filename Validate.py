
import sqlite3
import inspect
from Models.Scooter import Scooter
from Models.Traveller import Traveller
from Models.User import User
from datetime import date, datetime, timedelta
from permissions import Permissions
import re

#email is a standard python library, but might have to check if it's allowed
from email.utils import parseaddr 
from email.errors import HeaderParseError
from email.headerregistry import Address


class Validate:
    @staticmethod
    def Validate_user(user: User, New_user: User):
        New_user.username = Validate.validate_input("Enter username: ", username=user.username, custom_validator=Validate.is_valid_username)
        New_user.password = Validate.validate_input("Enter password: ", username=user.username, custom_validator=Validate.is_valid_password)
        New_user.first_name = Validate.validate_input("Enter first name: (2-20)", username=user.username, min_length=2, max_length=20)
        New_user.last_name = Validate.validate_input("Enter last name: (2-20)", username=user.username, min_length=2, max_length=20)
        return New_user
    
    @staticmethod
    def validate_updateuser(user: User, user_to_update: User):
        user_to_update.role = Validate.validate_input("change role: ", username=user.username, custom_validator=Validate.is_valid_role)
        user_to_update.username = Validate.validate_input("Change username: ", username=user.username, custom_validator=Validate.is_valid_username)
        user_to_update.first_name = Validate.validate_input("Change first name: (2-20)", username=user.username, min_length=2, max_length=20)
        user_to_update.last_name = Validate.validate_input("Change last name: (2-20)", username=user.username, min_length=2, max_length=20)
        return user_to_update
    
    @staticmethod
    def Validate_addscooter(user: User, scooter: Scooter):
        scooter.serial_number = Validate.validate_input("Enter serial number (unique 10-17 alphanumeric): ", username=user.username, custom_validator=Validate.is_valid_serialnumber)
        scooter.brand = Validate.validate_input("Enter brand: (1-20)", username=user.username, min_length=1, max_length=20)
        scooter.model = Validate.validate_input("Enter model: (1-20)", username=user.username, min_length=1, max_length=20)
        scooter.top_speed = Validate.validate_input("Enter top speed (km/h): ", username=user.username, custom_validator=Validate.is_valid_topspeed)
        scooter.battery_capacity = Validate.validate_input("Enter battery capacity (Wh): ", username=user.username, custom_validator=Validate.is_valid_battery_capacity)
        scooter.soc = Validate.validate_input("Enter state of charge (0-100): ", username=user.username, custom_validator=Validate.is_valid_soc)
        while True:
            min_soc = Validate.validate_input("Enter target range SOC min (0-100): ", username=user.username)
            max_soc = Validate.validate_input("Enter target range SOC max (0-100): ", username=user.username)
            if Validate.is_valid_target_soc(min_soc, max_soc):
                scooter.target_range_soc = (min_soc, max_soc)
                break
            print("Invalid target range SOC. Ensure 0 <= min < max <= 100.")
        while True:
            latitude = Validate.validate_input("Enter latitude (51.85000 - 51.99000, 5 decimals): ", username=user.username)
            longitude = Validate.validate_input("Enter longitude (4.40000 - 4.60000, 5 decimals): ", username=user.username)
            if Validate.is_valid_location(latitude, longitude):
                scooter.location = (latitude, longitude)
                break
            print("Invalid location. Ensure latitude is between 51.85000 and 51.99000, and longitude is between 4.40000 and 4.60000, both with 5 decimal places.")
        scooter.out_of_service = Validate.validate_input("Is the scooter out of service? (1 for true/0 for false): ", username=user.username, custom_validator=Validate.is_valid_out_of_service)
        scooter.mileage = Validate.validate_input("Enter mileage: ", username=user.username, custom_validator=Validate.is_valid_mileage)
        scooter.last_maintenance_date = datetime.today().strftime("%Y-%m-%d")
        return scooter
    
    def Validate_addtraveller(user: User, traveller: Traveller):
        traveller.first_name = Validate.validate_input("Enter first name (2-20): ", username=user.username, min_length=2, max_length=20)
        traveller.last_name = Validate.validate_input("Enter last name (2-20): ", username=user.username, min_length=2, max_length=20)
        birthday_str = Validate.validate_input("Enter birth date (YYYY-MM-DD): ", username=user.username, custom_validator=Validate.is_valid_birthdate, min_length=10, max_length=10)
        traveller.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        traveller.gender = Validate.validate_input("Enter gender (male/female): ", username=user.username, custom_validator=Validate.is_valid_gender, min_length=4, max_length=6)
        traveller.street_name = Validate.validate_input("Enter street name: ", username=user.username, min_length=1, max_length=100)
        traveller.house_number = Validate.validate_input("Enter house number with unit/apartment number: ", username=user.username, min_length=1, max_length=20) #20 is likely too much but there can be lengthy designators
        traveller.zip_code = Validate.validate_input("Enter dutch zipcode (DDDDXX): ", username=user.username, custom_validator=Validate.is_valid_zip_code, min_length=6, max_length=7) #regex handles optional space so allow max 7
        
        cities = ["Rotterdam", "Amsterdam", "Den Haag", "Utrecht", "Delft", "Eindhoven", "Groningen", "Maastricht", "Zwolle", "Nijmegen"]
        #The system should generate a list of 10 predefined city names of your choice.
        print("Available cities:")
        for i in range(1, 10):
            print(f"{i}. {cities[i-1]}")

        traveller.city = cities[int(Validate.validate_input("Select a city: ", custom_validator=Validate.is_digit,  min_length=1, max_length=2, )) - 1]
        traveller.email_address = Validate.validate_input("Enter email address: ", username=user.username, custom_validator=Validate.is_valid_email, min_length=3, max_length=254)
        traveller.mobile_phone = "+31-6-" + Validate.validate_input("Enter phone number: +31-6-", custom_validator=Validate.is_digit, min_length=8, max_length=8)
        traveller.driving_license_number = Validate.validate_input("Enter driving license number: ", custom_validator=Validate.is_valid_driving_license_number, min_length=9, max_length=9)
        
        return traveller
    
    @staticmethod
    def validate_updatescooter_engineer(user: User, scooter: Scooter):
        scooter.soc = Validate.validate_input("Enter new SOC (0-100): ", username=user.username, custom_validator=Validate.is_valid_soc)
        while True:
            min_soc = Validate.validate_input("Enter new target range SOC min (0-100): ", username=user.username)
            max_soc = Validate.validate_input("Enter new target range SOC max (0-100): ", username=user.username)
            if Validate.is_valid_target_soc(min_soc, max_soc):
                scooter.target_range_soc = (min_soc, max_soc)
                break
            print("Invalid target range SOC. Ensure 0 <= min < max <= 100.")
        while True:
            latitude = Validate.validate_input("Enter new latitude (51.85000 - 51.99000, 5 decimals): ", username=user.username)
            longitude = Validate.validate_input("Enter new longitude (4.40000 - 4.60000, 5 decimals): ", username=user.username)
            if Validate.is_valid_location(latitude, longitude):
                scooter.location = (latitude, longitude)
                break
            print("Invalid location. Ensure latitude is between 51.85000 and 51.99000, and longitude is between 4.40000 and 4.60000, both with 5 decimal places.")
        scooter.out_of_service = Validate.validate_input("Is the scooter out of service? (1 for true/0 for false): ", username=user.username, custom_validator=Validate.is_valid_out_of_service)
        scooter.mileage = Validate.validate_input("Enter new mileage: ", username=user.username, custom_validator=Validate.is_valid_mileage)
        scooter.last_maintenance_date = Validate.validate_input("Enter new last maintenance date (YYYY-MM-DD): ", username=user.username, custom_validator=lambda d: Validate.is_valid_last_maintenance_date(d, scooter=scooter))
        return scooter

    @staticmethod
    def validate_updatescooter_admin(user: User, scooter: Scooter):
        scooter.serial_number = Validate.validate_input("Enter serial number (unique 10-17 alphanumeric): ", username=user.username, custom_validator=Validate.is_valid_serialnumber)
        scooter.brand = Validate.validate_input("Enter brand: (1-20)", username=user.username, min_length=1, max_length=20)
        scooter.model = Validate.validate_input("Enter model: (1-20)", username=user.username, min_length=1, max_length=20)
        scooter.top_speed = Validate.validate_input("Enter top speed (km/h): ", username=user.username, custom_validator=Validate.is_valid_topspeed)
        scooter.battery_capacity = Validate.validate_input("Enter battery capacity (Wh): ", username=user.username, custom_validator=Validate.is_valid_battery_capacity)
        scooter.soc = Validate.validate_input("Enter new SOC (0-100): ", username=user.username, custom_validator=Validate.is_valid_soc)
        while True:
            min_soc = Validate.validate_input("Enter new target range SOC min (0-100): ", username=user.username)
            max_soc = Validate.validate_input("Enter new target range SOC max (0-100): ", username=user.username)
            if Validate.is_valid_target_soc(min_soc, max_soc):
                scooter.target_range_soc = (min_soc, max_soc)
                break
            print("Invalid target range SOC. Ensure 0 <= min < max <= 100.")
        while True:
            latitude = Validate.validate_input("Enter new latitude (51.85000 - 51.99000, 5 decimals): ", username=user.username)
            longitude = Validate.validate_input("Enter new longitude (4.40000 - 4.60000, 5 decimals): ", username=user.username)
            if Validate.is_valid_location(latitude, longitude):
                scooter.location = (latitude, longitude)
                break
            print("Invalid location. Ensure latitude is between 51.85000 and 51.99000, and longitude is between 4.40000 and 4.60000, both with 5 decimal places.")
        scooter.out_of_service = Validate.validate_input("Is the scooter out of service? (1 for true/0 for false): ", username=user.username, custom_validator=Validate.is_valid_out_of_service)
        scooter.mileage = Validate.validate_input("Enter new mileage: ", username=user.username, custom_validator=Validate.is_valid_mileage)
        scooter.last_maintenance_date = Validate.validate_input("Enter new last maintenance date (YYYY-MM-DD): ", username=user.username, custom_validator=lambda d: Validate.is_valid_last_maintenance_date(d, scooter=scooter))
        return scooter
    
    @staticmethod
    def is_valid_role(role):
        dummy_user = User()
        dummy_user.role = role
        # Only return True if the role has the "valid_role_assignment" permission
        return Permissions.has_permission(dummy_user, "valid_role_assignment")

    @staticmethod
    def is_valid_username(username):
        from Utils import Utility
        if not Utility.fetch_userinfo(username, check_username=True):
            return False  # Username exists
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_'.]{8,10}$"
        return bool(re.fullmatch(pattern, username, re.IGNORECASE))
     
    @staticmethod
    def is_valid_password(password):
        # Length check
        if not (12 <= len(password) <= 30):
            return False

        # Allowed characters
        allowed_pattern = r"^[a-zA-Z0-9~!@#$%&_\-\+=`|\\\(\)\{\}\[\]:;'<>,\.?\/]+$"
        if not re.fullmatch(allowed_pattern, password):
            return False

        # At least one lowercase, one uppercase, one digit, one special character
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[~!@#$%&_\-\+=`|\\\(\)\{\}\[\]:;'<>,\.?\/]", password):
            return False

        return True
    
    @staticmethod
    def is_valid_serialnumber(serial_number):
        if not re.fullmatch(r"[a-zA-Z0-9]{10,16}", serial_number):
            return False
        conn = sqlite3.connect('scooters.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM scooters WHERE serial_number = ?", (serial_number,))
        exists = c.fetchone()[0] > 0
        conn.close()
        if exists:
            return False
        return True

    @staticmethod
    def is_valid_topspeed(top_speed):
        if not re.fullmatch(r"\d{1,3}", str(top_speed)):
            return False
        value = int(top_speed)
        return 1 <= value <= 200

    @staticmethod
    def is_valid_battery_capacity(battery_capacity):
        if not re.fullmatch(r"\d{3,4}", str(battery_capacity)):
            return False
        value = int(battery_capacity)
        return 100 <= value <= 3000

    @staticmethod
    def is_valid_soc(soc):
        if not re.fullmatch(r"\d{1,3}", str(soc)):
            return False
        value = int(soc)
        return 0 <= value <= 100
    
    @staticmethod
    def is_valid_target_soc(min_soc, max_soc):
        if not re.fullmatch(r"\d{1,3}", str(min_soc)) or not re.fullmatch(r"\d{1,3}", str(max_soc)):
            return False
        min_value = int(min_soc)
        max_value = int(max_soc)
        return 0 <= min_value < max_value <= 100
    
    @staticmethod
    def is_valid_location(latitude, longitude):
        try:
            lat = float(latitude)
            lon = float(longitude)
        except ValueError:
            return False

        # Check latitude range and 5 decimal places
        if not (51.85000 <= lat <= 51.99000):
            return False
        if not (4.40000 <= lon <= 4.60000):
            return False

        # Check longitude range and 5 decimal places
        if '.' not in str(latitude) or len(str(latitude).split('.')[-1]) != 5:
            return False
        if '.' not in str(longitude) or len(str(longitude).split('.')[-1]) != 5:
            return False

        return True
    
    @staticmethod
    def is_valid_out_of_service(out_of_service):
        if int(out_of_service) == 0 or int(out_of_service) == 1:
            return True
        return False
    
    @staticmethod
    def is_valid_mileage(mileage):
        try:
            value = float(mileage)
            return value >= 0.0
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_last_maintenance_date(date_str, scooter=None):
        try:
            # Check format and parse date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False

        today = datetime.today()
        fifty_years_ago = today - timedelta(days=50*365.25)

        # Must be in the past and not more than 50 years ago
        if not (fifty_years_ago <= date_obj < today):
            return False
        
        if scooter and not date_obj >= datetime.strptime(scooter.in_service_date, "%Y-%m-%d"):
            return False
        return True
    
    @staticmethod
    def is_valid_birthdate(date_str):
        try:
            # Check format and parse date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False
        
        today = datetime.today()

        if not (date_obj < today):
            return False
        return True
    
    @staticmethod
    def is_valid_gender(gender_char):
        if gender_char != "male" and gender_char != "female":
            return False
        return True
    
    @staticmethod
    def is_valid_zip_code(zip_code_str):
        pattern = r'^\d{4} ?[A-Z]{2}$'
        return bool(re.fullmatch(pattern, zip_code_str))
    
    @staticmethod
    def is_valid_email(email_str):
        pattern = r'^(?=.{6,254}$)[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,}$'
        if not bool(re.fullmatch(pattern, email_str)):
            return False
        
        try: #extra validation against RFC 5322 syntax rules.
            addr = Address(addr_spec=email_str)
            return True
        except HeaderParseError:
            return False
        
    @staticmethod
    def is_digit(input_str: str):
        return input_str.isdigit()
    
    @staticmethod
    def is_valid_driving_license_number(driving_licence_number_str):
        pattern = r'^(?:[A-Z]{2}\d{7}|[A-Z]{1}\d{8})$'
        return bool(re.fullmatch(pattern, driving_licence_number_str))

    
    @staticmethod
    def validate_input(
        prompt: str,
        min_length: int = 1,
        max_length: int = 255,
        allow_null_byte: bool = False,
        custom_validator=None,
        username: str = "",
        activity: str = "Input validation failed",
        additional_info: str = ""
    ):
        from Utils import Utility
        suspicious_count = 0

        validator_name = custom_validator.__name__ if custom_validator else ""
        caller_name = inspect.stack()[1].function
        if not additional_info and validator_name:
            additional_info = f"{caller_name} -> {validator_name}"

        while True:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty.")
                suspicious_count += 1
                Utility.log_activity(username, activity, additional_info, suspicious_count)
                continue
            if not allow_null_byte and '\x00' in value:
                print("Input cannot contain null bytes.")
                suspicious_count += 1
                Utility.log_activity(username, activity, additional_info, suspicious_count)
                continue
            if not (min_length <= len(value) <= max_length):
                print(f"Input must be between {min_length} and {max_length} characters.")
                suspicious_count += 1
                Utility.log_activity(username, activity, additional_info, suspicious_count)
                continue
            if custom_validator and not custom_validator(value):
                print("Input failed validation.")
                suspicious_count += 1
                Utility.log_activity(username, activity, additional_info, suspicious_count)
                continue
            return value

    # Example usage:
    # username = validate_input("Enter username: ", min_length=8, max_length=10, custom_validator=Utility.is_valid_username)