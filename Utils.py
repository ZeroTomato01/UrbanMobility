import sqlite3
from Models.Scooter import Scooter
from Models.User import User
from cryptography.fernet import Fernet
from datetime import datetime

class Utility:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def Save_scooter(scooter: Scooter):
        conn = sqlite3.connect('scooters.db')
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO scooters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scooter.serial_number,
            scooter.brand,
            scooter.model,
            scooter.top_speed,
            scooter.battery_capacity,
            scooter.soc,
            scooter.target_range_soc[0],
            scooter.target_range_soc[1],
            scooter.location[0],
            scooter.location[1],
            int(scooter.out_of_service),
            scooter.mileage,
            scooter.last_maintenance_date.isoformat(),
            scooter.in_service_date.isoformat()
        ))
        conn.commit()
        conn.close()
    
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        with open("fernet.key", "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key():
        with open("fernet.key", "rb") as key_file:
            key = key_file.read()
        cipher_suite = Fernet(key)
        return cipher_suite
    
    @staticmethod
    def fetch_userinfo(username):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
            if decrypted_username == username:
                reg_date = datetime.strptime(row['registration_date'], "%Y-%m-%d").date()
                return User(
                    role=row['role'],
                    username=row['username'],
                    password=row['password'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    registration_date=reg_date
                )
        return None
    

    edit_permissions = {
        "brand": ["Super Administrator", "System Administrator"],
        "model": ["Super Administrator", "System Administrator"],
        "serial_number": ["Super Administrator", "System Administrator"],
        "top_speed": ["Super Administrator", "System Administrator"],
        "battery_capacity": ["Super Administrator", "System Administrator"],
        "soc": ["Super Administrator", "System Administrator", "Service Engineer"],
        "target_range_soc": ["Super Administrator", "System Administrator", "Service Engineer"],
        "location": ["Super Administrator", "System Administrator", "Service Engineer"],
        "out_of_service": ["Super Administrator", "System Administrator", "Service Engineer"],
        "mileage": ["Super Administrator", "System Administrator", "Service Engineer"],
        "last_maintenance_date": ["Super Administrator", "System Administrator", "Service Engineer"],
    }

    @staticmethod
    def get_roles_for_field(field: str):
        return Utility.edit_permissions.get(field, [])

    @staticmethod
    def can_edit(field: str, role: str) -> bool:
        return role in Utility.get_roles_for_field(field)