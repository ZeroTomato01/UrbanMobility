import sqlite3
from Models.Scooter import Scooter
from Models.User import User
from cryptography.fernet import Fernet
from datetime import datetime
import os
import zipfile
import re
import shutil

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
    def fetch_userinfo(username, check_username=False):
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
                if check_username:
                    return False  # Username exists
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
    def is_valid_username(username):
        if not Utility.fetch_userinfo(username, check_username=True):
            return False  # Username exists
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$"
        return bool(re.fullmatch(pattern, username, re.IGNORECASE))
    
    @staticmethod
    def is_valid_password(password):
        # Length check
        if not (12 <= len(password) <= 30):
            return False

        # Allowed characters
        allowed_pattern = r"^[a-zA-Z0-9~!@#$%&_\-\+=`|\\\(\)\{\}\[\]:;'<>,\.?\/]+$"
        if not re.fullmatch(allowed_pattern, password):
            return False

        # At least one lowercase, one uppercase, one digit, one special character
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[~!@#$%&_\-\+=`|\\\(\)\{\}\[\]:;'<>,\.?\/]", password):
            return False

        return True
