import sqlite3
from Models.Scooter import Scooter
from Models.User import User
from datetime import datetime, timedelta
import re

class Validate:
    @staticmethod
    def Validate_user(user: User):
        user.username = Validate.validate_input("Enter username: ", custom_validator=Validate.is_valid_username)
        user.password = Validate.validate_input("Enter password: ", custom_validator=Validate.is_valid_password)
        user.first_name = Validate.validate_input("Enter first name: ", min_length=2, max_length=20)
        user.last_name = Validate.validate_input("Enter last name: ", min_length=2, max_length=20)
        return user
    
    @staticmethod
    def Validate_scooter(scooter: Scooter):
        scooter.serial_number = Validate.validate_input("Enter serial number ( unique 10-17 alphanumeric): ", custom_validator=Validate.is_valid_serialnumber)
        scooter.brand = Validate.validate_input("Enter brand: ", min_length=1, max_length=20)
        scooter.model = Validate.validate_input("Enter model: ", min_length=1, max_length=20)
        scooter.top_speed = Validate.validate_input("Enter top speed (km/h): ", custom_validator=Validate.is_valid_topspeed)
        scooter.battery_capacity = Validate.validate_input("Enter battery capacity (Wh): ", custom_validator=Validate.is_valid_battery_capacity)
        scooter.soc = Validate.validate_input("Enter state of charge (0-100): ", custom_validator=Validate.is_valid_soc)
        while True:
            min_soc = Validate.validate_input("Enter target range SOC min (0-100): ")
            max_soc = Validate.validate_input("Enter target range SOC max (0-100): ")
            if Validate.is_valid_target_soc(min_soc, max_soc):
                scooter.target_range_soc = (min_soc, max_soc)
                break
            print("Invalid target SOC range. Try again.")
        while True:
            latitude = Validate.validate_input("Enter latitude (51.85000 - 51.99000, 5 decimals): ")
            longitude = Validate.validate_input("Enter longitude (4.40000 - 4.60000, 5 decimals): ")
            if Validate.is_valid_location(latitude, longitude):
                scooter.location = (float(latitude), float(longitude))
                break
            print("Invalid location. Try again.")
        scooter.out_of_service = Validate.validate_input("Is the scooter out of service? (1 for true/0 for false): ", custom_validator=Validate.is_valid_out_of_service)
        scooter.mileage = Validate.validate_input("Enter mileage: ", custom_validator=Validate.is_valid_mileage)
        scooter.last_maintenance_date = Validate.validate_input("Enter last maintenance date (YYYY-MM-DD): ", custom_validator=Validate.is_valid_last_maintenance_date)
        return scooter

    
    @staticmethod
    def is_valid_username(username):
        from Utils import Utility
        if not Utility.fetch_userinfo(username, check_username=True):
            return False  # Username exists
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$"
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
        if not re.fullmatch(r"[a-zA-Z0-9]{9,16}", serial_number):
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
        return True

    @staticmethod
    def is_valid_battery_capacity(battery_capacity):
        if not re.fullmatch(r"\d{3,4}", str(battery_capacity)):
            return False
        return True

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
        if not (round(lat, 5) == lat and len(str(lat).split('.')[-1]) == 5):
            return False

        # Check longitude range and 5 decimal places
        if not (4.40000 <= lon <= 4.60000):
            return False
        if not (round(lon, 5) == lon and len(str(lon).split('.')[-1]) == 5):
            return False

        return True
    
    @staticmethod
    def is_valid_out_of_service(out_of_service):
        if out_of_service == 0 or out_of_service == 1:
            return True
        return False
    
    @staticmethod
    def is_valid_mileage(mileage):
        try:
            value = float(mileage)
            return value >= 0
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_last_maintenance_date(date_str):
        try:
            # Check format and parse date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False

        today = datetime.today()
        fifty_years_ago = today - timedelta(days=50*365.25)

        # Must be in the past and not more than 50 years ago
        return fifty_years_ago <= date_obj < today
    
    @staticmethod
    def validate_input(
        prompt: str,
        min_length: int = 1,
        max_length: int = 255,
        allow_null_byte: bool = False,
        custom_validator=None
    ):
        while True:
            value = input(prompt)
            if not value:
                print("Input cannot be empty.")
                continue
            if not allow_null_byte and '\x00' in value:
                print("Input cannot contain null bytes.")
                continue
            if not (min_length <= len(value) <= max_length):
                print(f"Input must be between {min_length} and {max_length} characters.")
                continue
            if custom_validator and not custom_validator:
                print("Input failed custom validation.")
                continue
            return value

    # Example usage:
    # username = validate_input("Enter username: ", min_length=8, max_length=10, custom_validator=Utility.is_valid_username)