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
    def Add_scooter(user: User, scooter: Scooter):
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
            Utility.log_activity(user.username, "Add scooter to DB", additional_info="Scooter added to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error adding scooter to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            Utility.log_activity(user.username, "Add scooter to DB", additional_info=f"Add scooter to DB failed: {e}", suspicious_count = 3)
            return
    
    @staticmethod
    def Add_user(user: User, new_user: User):
        try:
            encrypt = Utility.load_key()
            enc_username = encrypt.encrypt(new_user.username.encode('utf-8'))
            hash_password = hashlib.sha256(new_user.password.encode('utf-8')).hexdigest()
            enc_first_name = encrypt.encrypt(new_user.first_name.encode('utf-8'))
            enc_last_name = encrypt.encrypt(new_user.last_name.encode('utf-8'))
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (role, username, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)
            ''', (
                new_user.role,
                enc_username,
                hash_password,
                enc_first_name,
                enc_last_name,
            ))
            conn.commit()
            conn.close()
            print("User added successfully.")
            Utility.log_activity(user.username, "Add user to DB", additional_info="User added to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error adding user to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            Utility.log_activity(user.username, "Add user to DB", additional_info=f"Add user to DB failed: {e}", suspicious_count = 3)
            return

    @staticmethod
    def log_activity(username, activity, additional_info="", suspicious_count = 0):
        suspicious = False
        if suspicious_count > 2:
            suspicious = True
        encrypt = Utility.load_key()
        enc_username = encrypt.encrypt(username.encode('utf-8'))
        enc_activity = encrypt.encrypt(activity.encode('utf-8'))
        enc_additional = encrypt.encrypt(additional_info.encode('utf-8'))
        try:
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
        except sqlite3.Error as e:
            print(f"log bricked woops: {e}")
    
    @staticmethod
    def print_logs(user: User):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('logs.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Order by id DESC for latest log on top
        c.execute("SELECT * FROM logs ORDER BY id DESC")
        logs = c.fetchall()

        print("No. | Date       | Time     | Username      | Activity Description         | Additional Info                               | Suspicious")
        print("-" * 135)
        for log in logs:
            username = encrypt.decrypt(log['username']).decode('utf-8')
            activity = encrypt.decrypt(log['activity']).decode('utf-8')
            additional_info = encrypt.decrypt(log['additional_info']).decode('utf-8') if log['additional_info'] else ""
            print(f"{log['id']:>3} | {log['date']} | {log['time']} | {username:<13} | {activity:<26} | {additional_info:<58} | {'Yes' if log['suspicious'] else 'No':<3}")

        # Set all unread logs to 0
        c.execute("UPDATE logs SET unread = 0 WHERE unread != 0")
        conn.commit()
        conn.close()
        Utility.log_activity(user.username, "Print logs", additional_info="User printed logs", suspicious_count = 0)

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
                brand=best_row['brand'],
                model=best_row['model'],
                serial_number=best_row['serial_number'],
                top_speed=best_row['top_speed'],
                battery_capacity=best_row['battery_capacity'],
                soc=best_row['soc'],
                target_range_soc=(best_row['target_range_soc_min'], best_row['target_range_soc_max']),
                location=(str(best_row['latitude']), str(best_row['longitude'])),
                out_of_service=bool(best_row['out_of_service']),
                mileage=float(best_row['mileage']),
                last_maintenance_date=best_row['last_maintenance_date'],
                in_service_date=best_row['in_service_date']
            )
            return scooter
        else:
            return None
    
    @staticmethod
    def fetch_searchuser(search_key):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM users")
        rows = c.fetchall()
        conn.close()

        search_key_lower = search_key.lower()
        best_score = -1
        best_row = None

        for row in rows:
            fields_to_search = [
                str(row['role']),
                str(encrypt.decrypt(row['username']).decode('utf-8')),
                str(encrypt.decrypt(row['first_name']).decode('utf-8') if row['first_name'] else row['first_name']),
                str(encrypt.decrypt(row['last_name']).decode('utf-8') if row['last_name'] else row['last_name']),
                str(row['registration_date']),
            ]
            # Score: count of fields containing the search key (higher is better)
            score = sum(search_key_lower in str(field).lower() for field in fields_to_search)
            if score > best_score:
                best_score = score
                best_row = row

        if best_row and best_score > 0:
            reg_date = datetime.strptime(best_row['registration_date'], "%Y-%m-%d").date()
            user = User(
                role=best_row['role'],
                username=encrypt.decrypt(best_row['username']).decode('utf-8') if best_row['username'] else "",
                password=best_row['password'] if best_row['password'] else "",
                first_name=encrypt.decrypt(best_row['first_name']).decode('utf-8') if best_row['first_name'] else "",
                last_name=encrypt.decrypt(best_row['last_name']).decode('utf-8') if best_row['last_name'] else "",
                registration_date=reg_date
            )
            return user
        else:
            return None
    
    @staticmethod
    def update_passwordDB(user: User, password, row_id):
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password = ? WHERE rowid = ?", (hash_password, row_id))
            conn.commit()
            conn.close()
            print("Password updated successfully.")
            Utility.log_activity(user.username, "Update password to DB", additional_info="Update password to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print(f"Error updating password in the database: {e}")
            Utility.log_activity(user.username, "Update password to DB", additional_info=f"Update password to DB failed: {e}", suspicious_count = 3)
            return
    
    @staticmethod
    def update_scooter_attributes_engineer(user: User, scooter: Scooter):
        scooter = Validate.validate_updatescooter_engineer(user, scooter)
        # Update the scooter in the database
        try:
            conn = sqlite3.connect('scooters.db')
            c = conn.cursor()
            c.execute('''
                UPDATE scooters SET
                    soc = ?,
                    target_range_soc_min = ?,
                    target_range_soc_max = ?,
                    latitude = ?,
                    longitude = ?,
                    out_of_service = ?,
                    mileage = ?,
                    last_maintenance_date = ?
                WHERE serial_number = ?
            ''', (
                scooter.soc,
                scooter.target_range_soc[0],
                scooter.target_range_soc[1],
                scooter.location[0],
                scooter.location[1],
                int(scooter.out_of_service),
                scooter.mileage,
                scooter.last_maintenance_date,
                scooter.serial_number
            ))
            conn.commit()
            conn.close()
            print("Scooter attributes updated successfully.")
            Utility.log_activity(user.username, "Update scooter to DB", additional_info="Update scooter to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error updating scooter in the database:", e)
            Utility.log_activity(user.username, "Update scooter to DB", additional_info=f"Update scooter to DB failed: {e}", suspicious_count = 3)

    @staticmethod
    def update_scooter_attributes_admin(user: User, scooter: Scooter):
        scooter = Validate.validate_updatescooter_admin(user, scooter)
        # Update the scooter in the database
        try:
            conn = sqlite3.connect('scooters.db')
            c = conn.cursor()
            c.execute('''
                UPDATE scooters SET
                    serial_number = ?,
                    brand = ?,
                    model = ?,
                    top_speed = ?,
                    battery_capacity = ?,
                    soc = ?,
                    target_range_soc_min = ?,
                    target_range_soc_max = ?,
                    latitude = ?,
                    longitude = ?,
                    out_of_service = ?,
                    mileage = ?,
                    last_maintenance_date = ?
                WHERE serial_number = ?
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
                scooter.last_maintenance_date,
                scooter.serial_number
            ))
            conn.commit()
            conn.close()
            print("Scooter attributes updated successfully.")
            Utility.log_activity(user.username, "Update scooter to DB", additional_info="Update scooter to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error updating scooter in the database:", e)
            Utility.log_activity(user.username, "Update scooter to DB", additional_info=f"Update scooter to DB failed: {e}", suspicious_count = 3)
    
    
    @staticmethod
    def create_backup(user: User):
        try:
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
            Utility.log_activity(user.username, "Backup of DB created", additional_info="Backup of DB creation successful", suspicious_count = 0)
            return backup_path
        except Exception as e:
            print(f"something went wrong backing up: {e}")
            Utility.log_activity(user.username, "Backup of DB created", additional_info="Backup of DB failed", suspicious_count = 3)



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
    def delete_user(user: User, delete_user: User):
        encrypt = Utility.load_key()

        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, username FROM users")
        rows = c.fetchall()

        target_rowid = None
        for row in rows:
            decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
            if decrypted_username == delete_user.username:
                target_rowid = row['rowid']
                break

        if target_rowid is not None:
            c.execute("DELETE FROM users WHERE rowid = ?", (target_rowid,))
            conn.commit()
            conn.close()
            print(f"User '{delete_user.username}' deleted successfully.")
            Utility.log_activity(user.username, "Delete user from DB", additional_info=f"Deleted user: {delete_user.username} from DB", suspicious_count = 0)
        else:
            print(f"User '{delete_user.username}' not found.")
            Utility.log_activity(user.username, "Delete user from DB", additional_info=f"Failed to delete user: {delete_user.username} from DB", suspicious_count = 3)
    
    @staticmethod
    def delete_scooterfromDB(user: User, scooter: Scooter):
        conn = sqlite3.connect('scooters.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Find the scooter by serial_number (which should be unique)
        c.execute("SELECT rowid FROM scooters WHERE serial_number = ?", (scooter.serial_number,))
        row = c.fetchone()

        if row is not None:
            c.execute("DELETE FROM scooters WHERE rowid = ?", (row['rowid'],))
            conn.commit()
            conn.close()
            print(f"Scooter '{scooter.serial_number}' deleted successfully.")
            Utility.log_activity(user.username, "Delete scooter from DB", additional_info=f"Deleted scooter: {scooter.serial_number} from DB", suspicious_count=0)
        else:
            conn.close()
            print(f"Scooter '{scooter.serial_number}' not found.")
            Utility.log_activity(user.username, "Delete scooter from DB", additional_info=f"Failed to delete scooter: {scooter.serial_number} from DB", suspicious_count=3)
    
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
        print(f"Target Range SOC Min: {scooter.target_range_soc[0]}")
        print(f"Target Range SOC Max: {scooter.target_range_soc[1]}")
        print(f"Latitude: {scooter.location[0]}")
        print(f"Longitude: {scooter.location[1]}")
        print(f"Out of Service: {'Yes' if scooter.out_of_service else 'No'}")
        print(f"Mileage: {scooter.mileage}")
        print(f"Last Maintenance Date: {scooter.last_maintenance_date}")
        print(f"In Service Date: {scooter.in_service_date}")
