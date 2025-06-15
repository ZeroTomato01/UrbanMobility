import sqlite3
from Models import Scooter
from cryptography.fernet import Fernet

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