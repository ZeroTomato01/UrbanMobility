from typing import Tuple, Dict, List
from datetime import date
from dataclasses import field, dataclass

@dataclass
class Scooter:
    brand: str = ""
    model: str = ""
    serial_number: str = ""  # 10-17 alphanumeric characters
    top_speed: str  = "" # km/h
    battery_capacity: str = ""  # Wh
    soc: str = "" # State of Charge (%)
    target_range_soc: Tuple[str, str] = ('', '') # (min%, max%)
    location: Tuple[str, str] = ("0.00000", "0.00000") # (latitude, longitude) 5 decimal places, must be within Rotterdam
    out_of_service: bool = True
    mileage: float = 0.0 # km
    last_maintenance_date: date = field(default = None) # ISO 8601 format YYYY-MM-DD
    in_service_date: date = field(default = None) # ISO 8601 format YYYY-MM-DD