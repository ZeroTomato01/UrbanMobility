from typing import Tuple, Dict, List
from datetime import date
from dataclasses import field

class Scooter:
    brand: str
    model: str
    serial_number: str  # 10-17 alphanumeric characters
    top_speed: str  # km/h
    battery_capacity: str  # Wh
    soc: str  # State of Charge (%)
    target_range_soc: Tuple[str, str]  # (min%, max%)
    location: Tuple[float, float]  # (latitude, longitude) 5 decimal places, must be within Rotterdam
    out_of_service: bool
    mileage: float  # km
    last_maintenance_date: date # ISO 8601 format YYYY-MM-DD
    in_service_date: date # ISO 8601 format YYYY-MM-DD

    # Permissions: attribute -> roles allowed to edit
    edit_permissions: Dict[str, List[str]] = field(default_factory=lambda: {
        "brand": ["Super Administrator", "System Administrator", "Service Engineer"],
        "model": ["Super Administrator", "System Administrator", "Service Engineer"],
        "serial_number": ["Super Administrator", "System Administrator"],
        "top_speed": ["Super Administrator", "System Administrator", "Service Engineer"],
        "battery_capacity": ["Super Administrator", "System Administrator", "Service Engineer"],
        "soc": ["Super Administrator", "System Administrator", "Service Engineer"],
        "target_range_soc": ["Super Administrator", "System Administrator", "Service Engineer"],
        "location": ["Super Administrator", "System Administrator", "Service Engineer"],
        "out_of_service": ["Super Administrator", "System Administrator", "Service Engineer"],
        "mileage": ["Super Administrator", "System Administrator", "Service Engineer"],
        "last_maintenance_date": ["Super Administrator", "System Administrator", "Service Engineer"],
    })

    def can_edit(self, attribute: str, role: str) -> bool:
        return role in self.edit_permissions.get(attribute, [])
