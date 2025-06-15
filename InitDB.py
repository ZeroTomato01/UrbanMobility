import sqlite3
import hashlib
from Utils import Utility

class InitDB:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def Init_travellerdb():
        conn = sqlite3.connect('traveller.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS travellers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birthday TEXT NOT NULL,
                gender TEXT CHECK(gender IN ('male', 'female')) NOT NULL,
                street_name TEXT NOT NULL,
                house_number TEXT NOT NULL,
                zip_code TEXT CHECK(zip_code GLOB '????[A-Z][A-Z]') NOT NULL,
                city TEXT NOT NULL,
                email_address TEXT NOT NULL,
                mobile_phone TEXT CHECK(mobile_phone GLOB '+31-6-????????') NOT NULL,
                driving_license_number TEXT CHECK(
                    driving_license_number GLOB '[A-Z][A-Z]???????' OR
                    driving_license_number GLOB '[A-Z]????????'
                ) NOT NULL,
                registration_date TEXT DEFAULT (datetime('now'))
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def Init_userdb():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                role TEXT NOT NULL,
                username TEXT NOT NULL PRIMARY KEY,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                registration_date TEXT DEFAULT (date('now'))
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
            INSERT OR REPLACE INTO users (role, username, password) VALUES (?, ?, ?)
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
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                top_speed REAL CHECK(top_speed > 0),
                battery_capacity str,
                soc str,
                target_range_soc_min str,
                target_range_soc_max str,
                latitude REAL
                    CHECK(latitude >= 51.85000 AND latitude <= 51.99000)
                    CHECK(CAST(latitude * 100000 AS INTEGER) = latitude * 100000)
                    CHECK(CAST(latitude * 10000 AS INTEGER) != latitude * 10000),
                longitude REAL
                    CHECK(longitude >= 4.40000 AND longitude <= 4.60000)
                    CHECK(CAST(longitude * 100000 AS INTEGER) = longitude * 100000)
                    CHECK(CAST(longitude * 10000 AS INTEGER) != longitude * 10000),
                out_of_service INTEGER CHECK(out_of_service IN (0, 1)) DEFAULT 0,
                mileage REAL CHECK(mileage >= 0),
                last_maintenance_date TEXT,
                in_service_date TEXT DEFAULT (datetime('now'))
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
    
    @staticmethod
    def Del_travellerdb():
        conn = sqlite3.connect('traveller.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS travellers')
        conn.commit()
        conn.close()