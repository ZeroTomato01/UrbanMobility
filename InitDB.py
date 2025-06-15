import sqlite3
import hashlib
from cryptography.fernet import Fernet
from Utils import Utility

class InitDB:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def Init_userdb():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                role TEXT,
                username TEXT PRIMARY KEY,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                registration_date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def Init_SAdb():
        SArole = "Super Administrator"
        SApassword = "Admin_123?"
        SAusername = "super_admin"
        encrypt = Utility.load_key()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO users VALUES (?, ?, ?)
        ''', (
            SArole,
            encrypt.encrypt(SAusername.encode('utf-8')),
            hashlib.sha256(SApassword.encode('utf-8')).hexdigest(),
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def Init_scooterdb():
        conn = sqlite3.connect('scooters.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scooters (
                serial_number TEXT PRIMARY KEY,
                brand TEXT,
                model TEXT,
                top_speed str,
                battery_capacity str,
                soc str,
                target_range_soc_min str,
                target_range_soc_max str,
                latitude REAL,
                longitude REAL,
                out_of_service INTEGER,
                mileage REAL,
                last_maintenance_date TEXT
                in_service_date TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    @staticmethod
    def Del_scooterdb():
        conn = sqlite3.connect('scooters.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS scooters')
        conn.commit()
        conn.close()
    
    @staticmethod
    def Del_userdb():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS users')
        conn.commit()
        conn.close()