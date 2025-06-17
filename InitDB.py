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
                registration_date TEXT DEFAULT (date('now'))
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
                latitude TEXT NOT NULL,
                longitude TEXT NOT NULL,
                out_of_service INTEGER CHECK(out_of_service IN (0, 1)) DEFAULT 0,
                mileage REAL CHECK(mileage >= 0),
                last_maintenance_date TEXT,
                in_service_date TEXT DEFAULT (date('now'))
            )
        ''')
        conn.commit()
        conn.close()
    
    @staticmethod
    def Init_logdb():
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT DEFAULT (date('now')),
                time TEXT DEFAULT (time('now')),
                username TEXT,
                activity TEXT NOT NULL,
                additional_info TEXT,
                suspicious INTEGER NOT NULL DEFAULT 0,
                unread INTEGER NOT NULL DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def Del_logdb():
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS logs')
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