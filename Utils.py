import sqlite3
from Models.Scooter import Scooter
from Models.User import User
from cryptography.fernet import Fernet
from datetime import datetime
from Validate import Validate
import os
import zipfile
import shutil
import hashlib

class Utility:
    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated directly.")
    
    @staticmethod
    def Add_scooter(scooter: Scooter):
        try:
            conn = sqlite3.connect('scooters.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO scooters (
                    serial_number, brand, model, top_speed, battery_capacity, soc,
                    target_range_soc_min, target_range_soc_max,
                    latitude, longitude, out_of_service, mileage,
                    last_maintenance_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                scooter.serial_number,
                scooter.brand,
                scooter.model,
                float(scooter.top_speed),
                scooter.battery_capacity,
                scooter.soc,
                scooter.target_range_soc[0],  # min
                scooter.target_range_soc[1],  # max
                scooter.location[0],          # latitude
                scooter.location[1],          # longitude
                int(scooter.out_of_service),
                scooter.mileage,
                scooter.last_maintenance_date,
            ))
            conn.commit()
            conn.close()
            print("Scooter added successfully.")
        except sqlite3.Error as e:
            print("Error adding scooter to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            return
    
    @staticmethod
    def Add_user(user):
        try:
            encrypt = Utility.load_key()
            enc_username = encrypt.encrypt(user.username.encode('utf-8'))
            hash_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
            enc_first_name = encrypt.encrypt(user.first_name.encode('utf-8'))
            enc_last_name = encrypt.encrypt(user.last_name.encode('utf-8'))
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (role, username, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)
            ''', (
                user.role,
                enc_username,
                hash_password,
                enc_first_name,
                enc_last_name,
            ))
            conn.commit()
            conn.close()
            print("User added successfully.")
        except sqlite3.Error as e:
            print("Error adding user to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            return

    @staticmethod
    def log_activity(username, activity, additional_info="", suspicious=False):
        encrypt = Utility.load_key()
        enc_username = encrypt.encrypt(username.encode('utf-8'))
        enc_activity = encrypt.encrypt(activity.encode('utf-8'))
        enc_additional = encrypt.encrypt(additional_info.encode('utf-8'))

        conn = sqlite3.connect('logs.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO logs (username, activity, additional_info, suspicious, unread)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            enc_username,
            enc_activity,
            enc_additional,
            1 if suspicious else 0, # 1 for true, 0 for false
            1  # unread by default
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
    def fetch_userinfo(username, check_username=False, row_id=False):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM users")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
            if decrypted_username == username:
                reg_date = datetime.strptime(row['registration_date'], "%Y-%m-%d").date()
                if check_username:
                    return False  # Username exists
                if row_id:
                    return row['rowid']
                return User(
                    role=row['role'],
                    username=encrypt.decrypt(row['username']).decode('utf-8'),
                    password=row['password'],
                    first_name=encrypt.decrypt(row['first_name']).decode('utf-8') if row['first_name'] else row['first_name'],
                    last_name=encrypt.decrypt(row['last_name']).decode('utf-8') if row['last_name'] else row['last_name'],
                    registration_date=reg_date
                )
        if check_username:
            return True
        return None
    
    @staticmethod
    def fetch_scooter_info(search_key):
        conn = sqlite3.connect('scooters.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM scooters")
        rows = c.fetchall()
        conn.close()

        search_key_lower = search_key.lower()
        best_score = -1
        best_row = None

        for row in rows:
            fields_to_search = [
                str(row['serial_number']),
                str(row['brand']),
                str(row['model']),
                str(row['top_speed']),
                str(row['battery_capacity']),
                str(row['soc']),
                str(row['mileage']),
                str(row['last_maintenance_date']),
                str(row['in_service_date']),
            ]
            # Score: count of fields containing the search key (higher is better)
            score = sum(search_key_lower in str(field).lower() for field in fields_to_search)
            if score > best_score:
                best_score = score
                best_row = row

        if best_row and best_score > 0:
            scooter = Scooter(
                serial_number=best_row['serial_number'],
                brand=best_row['brand'],
                model=best_row['model'],
                top_speed=best_row['top_speed'],
                battery_capacity=best_row['battery_capacity'],
                soc=best_row['soc'],
                target_range_soc_min=best_row['target_range_soc_min'],
                target_range_soc_max=best_row['target_range_soc_max'],
                latitude=best_row['latitude'],
                longitude=best_row['longitude'],
                out_of_service=best_row['out_of_service'],
                mileage=best_row['mileage'],
                last_maintenance_date=best_row['last_maintenance_date'],
                in_service_date=best_row['in_service_date']
            )
            return scooter, best_row['rowid']
        else:
            return None, None
    
    @staticmethod
    def update_passwordDB(password, row_id):
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password = ? WHERE rowid = ?", (hash_password, row_id))
            conn.commit()
            conn.close()
            print("Password updated successfully.")
        except sqlite3.Error:
            print("Error updating password in the database.")
            return
    
    @staticmethod
    def update_scooter_attributes(user: User, scooter: Scooter):
        return True

    

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
    
    @staticmethod
    def create_backup():
        db_files = ['users.db', 'scooters.db', 'traveller.db']
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_{timestamp}.zip'
        backup_path = os.path.join(backup_dir, backup_filename)

        with zipfile.ZipFile(backup_path, 'w') as backup_zip:
            for db_file in db_files:
                if os.path.exists(db_file):
                    backup_zip.write(db_file)
                else:
                    print(f"Warning: {db_file} not found and will not be included in the backup.")

        print(f"Backup created: {backup_path}")
        return backup_path
    
    @staticmethod
    def restore_backup(backup_zip_path):
        """
        Replace the current databases with those from the given backup zip file.
        """
        db_files = ['users.db', 'scooters.db', 'traveller.db']

        # Extract backup zip to a temporary directory
        temp_dir = "temp_restore"
        os.makedirs(temp_dir, exist_ok=True)
        with zipfile.ZipFile(backup_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Replace each db file with the one from the backup
        for db_file in db_files:
            backup_db_path = os.path.join(temp_dir, db_file)
            if os.path.exists(backup_db_path):
                shutil.copy2(backup_db_path, db_file)
                print(f"Restored {db_file} from backup.")
            else:
                print(f"Warning: {db_file} not found in backup and was not restored.")

        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print("Restore complete.")
    
    @staticmethod
    def print_userinfo(user: User):
        print("=== User Information ===")
        print(f"Role: {user.role}")
        print(f"Username: {user.username}")
        print(f"First Name: {user.first_name}")
        print(f"Last Name: {user.last_name}")
        print(f"Registration Date: {user.registration_date.isoformat()}")
    
    @staticmethod
    def print_scooterinfo(scooter: Scooter):
        print("=== Scooter Information ===")
        print(f"Serial Number: {scooter.serial_number}")
        print(f"Brand: {scooter.brand}")
        print(f"Model: {scooter.model}")
        print(f"Top Speed: {scooter.top_speed}")
        print(f"Battery Capacity: {scooter.battery_capacity}")
        print(f"State of Charge (SOC): {scooter.soc}")
        print(f"Target Range SOC Min: {scooter.target_range_soc_min}")
        print(f"Target Range SOC Max: {scooter.target_range_soc_max}")
        print(f"Latitude: {scooter.latitude}")
        print(f"Longitude: {scooter.longitude}")
        print(f"Out of Service: {'Yes' if scooter.out_of_service else 'No'}")
        print(f"Mileage: {scooter.mileage}")
        print(f"Last Maintenance Date: {scooter.last_maintenance_date}")
        print(f"In Service Date: {scooter.in_service_date}")
