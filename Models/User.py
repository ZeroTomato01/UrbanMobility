from datetime import date
from dataclasses import dataclass, field

@dataclass
class User:
    role: str = "" # User role: "Super Administrator", "System Administrator", "Service Engineer"
    username: str = "" # cryptographically secure username
    password: str = "" # Hashed password
    first_name: str = ""
    last_name: str = ""
    registration_date: date = field(default = None)
    restore_code: str = None  # only used for System Administrators