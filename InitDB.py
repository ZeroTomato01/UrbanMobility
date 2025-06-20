import sqlite3
import hashlib
from Utils import Utility

class InitDB:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def Init_travellerdb():
        conn = sqlite3.connect('travellers.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS travellers (
                first_name TEXT NOT NULL, 
                last_name TEXT NOT NULL,
                birthday TEXT NOT NULL,
                gender TEXT NOT NULL,
                street_name TEXT NOT NULL,
                house_number TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                city TEXT NOT NULL,
                email_address TEXT NOT NULL,
                mobile_phone TEXT NOT NULL,
                driving_license_number TEXT NOT NULL,
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
                registration_date TEXT DEFAULT (date('now')),
                Temp_password TEXT,
                restore_code TEXT,
                Locked INTEGER CHECK(Locked IN (0, 1)) DEFAULT 0 
            )
        ''')
        conn.commit()
        conn.close()
    # 1 for true, 0 for false
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
    def Init_dummyscooters():
        dummy_scooters = [
        {
            "serial_number": "SCOOTER0001A",
            "brand": "Yamaha",
            "model": "Neo",
            "top_speed": 45,
            "battery_capacity": 1200,
            "soc": "80",
            "target_range_soc_min": "20",
            "target_range_soc_max": "90",
            "latitude": "51.86001",
            "longitude": "4.50001",
            "out_of_service": 0,
            "mileage": 1500.5,
            "last_maintenance_date": "2024-06-01",
            "in_service_date": "2023-05-01"
        },
        {
            "serial_number": "SCOOTER0002B",
            "brand": "Segway",
            "model": "Ninebot",
            "top_speed": 25,
            "battery_capacity": 500,
            "soc": "60",
            "target_range_soc_min": "10",
            "target_range_soc_max": "80",
            "latitude": "51.90012",
            "longitude": "4.55012",
            "out_of_service": 1,
            "mileage": 800.0,
            "last_maintenance_date": "2024-05-15",
            "in_service_date": "2022-09-10"
        }
        ]

        conn = sqlite3.connect('scooters.db')
        c = conn.cursor()
        for s in dummy_scooters:
            c.execute('''
                INSERT OR IGNORE INTO scooters (
                    serial_number, brand, model, top_speed, battery_capacity, soc,
                    target_range_soc_min, target_range_soc_max, latitude, longitude,
                    out_of_service, mileage, last_maintenance_date, in_service_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                s["serial_number"], s["brand"], s["model"], s["top_speed"], str(s["battery_capacity"]), s["soc"],
                s["target_range_soc_min"], s["target_range_soc_max"], s["latitude"], s["longitude"],
                s["out_of_service"], s["mileage"], s["last_maintenance_date"], s["in_service_date"]
            ))
        conn.commit()
        conn.close()
    
    @staticmethod
    def Init_dummyusers():
        encrypt = Utility.load_key()

        dummy_users = [
            {
                "role": "System Administrator",
                "username": "admin_user1",
                "password": "AdminUser1_123!",
                "first_name": "Alice",
                "last_name": "Smith"
            },
            {
                "role": "Service Engineer",
                "username": "engineer01",
                "password": "Engineer01_456!",
                "first_name": "Bob",
                "last_name": "Johnson"
            }
        ]

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        for u in dummy_users:
            enc_username = encrypt.encrypt(u["username"].encode('utf-8'))
            hash_password = hashlib.sha256(u["password"].encode('utf-8')).hexdigest()
            enc_first_name = encrypt.encrypt(u["first_name"].encode('utf-8'))
            enc_last_name = encrypt.encrypt(u["last_name"].encode('utf-8'))
            c.execute('''
                INSERT OR IGNORE INTO users (role, username, password, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                u["role"], enc_username, hash_password, enc_first_name, enc_last_name
            ))
        conn.commit()
        conn.close()
    
    @staticmethod
    def Init_dummytravellers():
        encrypt = Utility.load_key()

        dummy_travellers = [
            {
                "first_name": "Charlie",
                "last_name": "Brown",
                "birthday": "1990-05-15",
                "gender": "male",
                "street_name": "Mainstreet",
                "house_number": "12A",
                "zip_code": "1234AB",
                "city": "Rotterdam",
                "email_address": "charlie.brown@example.com",
                "mobile_phone": "+31-6-12345678",
                "driving_license_number": "AB1234567"
            },
            {
                "first_name": "Daisy",
                "last_name": "Miller",
                "birthday": "1985-11-23",
                "gender": "female",
                "street_name": "Second Ave",
                "house_number": "34B",
                "zip_code": "5678CD",
                "city": "Rotterdam",
                "email_address": "daisy.miller@example.com",
                "mobile_phone": "+31-6-87654321",
                "driving_license_number": "C12345678"
            }
        ]

        conn = sqlite3.connect('travellers.db')
        c = conn.cursor()
        for t in dummy_travellers:
            encrypted_fields = [encrypt.encrypt(str(t[field]).encode('utf-8')) for field in [
                "first_name", "last_name", "birthday", "gender", "street_name", "house_number",
                "zip_code", "city", "email_address", "mobile_phone", "driving_license_number"
            ]]
            c.execute('''
                INSERT OR IGNORE INTO travellers (
                    first_name, last_name, birthday, gender, street_name, house_number,
                    zip_code, city, email_address, mobile_phone, driving_license_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', encrypted_fields)
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
        conn = sqlite3.connect('travellers.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS travellers')
        conn.commit()
        conn.close()