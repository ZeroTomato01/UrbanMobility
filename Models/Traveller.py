from typing import Tuple, Dict, List
from datetime import date
from dataclasses import field, dataclass

@dataclass
class Traveller:
    first_name: str = ""
    last_name: str = ""
    birthday: date = field(default = None) # ISO 8601 format YYYY-MM-DD
    gender: str = ""
    street_name: str  = ""
    house_number: str = ""
    zip_code: str = ""
    city: str = ""
    email_address: str = ""
    mobile_phone: str = ""
    driving_license_number: str = ""
    registration_date: date = field(default = None)
