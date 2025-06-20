import sqlite3
from Models.Traveller import Traveller
from Models.Scooter import Scooter
from Models.User import User
from cryptography.fernet import Fernet
from datetime import date, datetime
from Validate import Validate
import os
import zipfile
import shutil
import hashlib
import copy
import string
import secrets


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
            Utility.log_activity(user.username, "Add scooter to DB", additional_info=f"Scooter: {scooter.serial_number} added to DB", suspicious_count = 0)
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
            Utility.log_activity(user.username, "Add user to DB", additional_info=f"User: {new_user.username} added to DB", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error adding user to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            Utility.log_activity(user.username, "Add user to DB", additional_info=f"Add user to DB failed: {e}", suspicious_count = 3)
            return

    @staticmethod
    def Add_traveller(user: User, traveller: Traveller):
        try:
            encrypt = Utility.load_key()
            enc_first_name = encrypt.encrypt(traveller.first_name.encode('utf-8'))
            enc_last_name = encrypt.encrypt(traveller.last_name.encode('utf-8'))
            enc_birthday = encrypt.encrypt(traveller.birthday.isoformat().encode('utf-8'))
            enc_gender = encrypt.encrypt(traveller.gender.encode('utf-8'))
            enc_street_name = encrypt.encrypt(traveller.street_name.encode('utf-8'))
            enc_house_number = encrypt.encrypt(traveller.house_number.encode('utf-8'))
            enc_zip_code = encrypt.encrypt(traveller.zip_code.encode('utf-8'))
            enc_city = encrypt.encrypt(traveller.city.encode('utf-8'))
            enc_email_address = encrypt.encrypt(traveller.email_address.encode('utf-8'))
            enc_mobile_phone = encrypt.encrypt(traveller.mobile_phone.encode('utf-8'))
            enc_driving_license_number = encrypt.encrypt(traveller.driving_license_number.encode('utf-8'))


            conn = sqlite3.connect('travellers.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO travellers (
                    first_name, last_name, birthday, gender, street_name, house_number,
                    zip_code, city, email_address, mobile_phone, driving_license_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                enc_first_name,
                enc_last_name,
                enc_birthday,
                enc_gender,
                enc_street_name,
                enc_house_number,
                enc_zip_code,
                enc_city,
                enc_email_address,
                enc_mobile_phone,
                enc_driving_license_number
            ))
            conn.commit()
            conn.close()
            print("Traveller added successfully.")
            Utility.log_activity(user.username, "Add traveller to DB", additional_info=f"Traveller: {traveller.first_name} {traveller.last_name}, {traveller.zip_code} {traveller.city} added to DB", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error adding traveller to the database. Please check the input values.")
            print(f"SQLite error: {e}")
            Utility.log_activity(user.username, "Add traveller to DB", additional_info=f"Add traveller to DB failed: {e}", suspicious_count = 3)
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
                    username=decrypted_username,
                    password=row['password'],
                    first_name=encrypt.decrypt(row['first_name']).decode('utf-8') if row['first_name'] else "",
                    last_name=encrypt.decrypt(row['last_name']).decode('utf-8') if row['last_name'] else "",
                    registration_date=reg_date,
                    restore_code=row['restore_code'] if 'restore_code' in row.keys() else None,
                    temp_password=encrypt.decrypt(row['temp_password']).decode('utf-8') if row['temp_password'] else None,
                    locked=row['locked']
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
    def fetch_searchuser(search_key, role=None):
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
            if role and row['role'].lower() != role.lower():
                continue
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
                registration_date=reg_date,
                restore_code=row['restore_code'] if 'restore_code' in row.keys() else None,
                temp_password=encrypt.decrypt(row['temp_password']).decode('utf-8') if row['temp_password'] else None,
                locked=row['locked']
            )
            return user
        else:
            return None
        
    @staticmethod
    def fetch_search_traveller(search_key):
        encrypt = Utility.load_key()
        conn = sqlite3.connect('travellers.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM travellers")
        rows = c.fetchall()
        conn.close()

        search_key_lower = search_key.lower()
        best_score = -1
        best_row = None

        for row in rows:
            # if role and row['role'].lower() != role.lower():
            #     continue
            fields_to_search = [
                
                str(encrypt.decrypt(row['first_name']).decode('utf-8') if row['first_name'] else row['first_name']),
                str(encrypt.decrypt(row['last_name']).decode('utf-8') if row['last_name'] else row['last_name']),
                str(datetime.strptime(encrypt.decrypt(row['birthday']).decode('utf-8'), "%Y-%m-%d").date())
                if row['birthday'] else '',
                str(encrypt.decrypt(row['gender']).decode('utf-8') if row['gender'] else row['gender']),
                str(encrypt.decrypt(row['street_name']).decode('utf-8') if row['street_name'] else row['street_name']),
                str(encrypt.decrypt(row['house_number']).decode('utf-8') if row['house_number'] else row['house_number']),
                str(encrypt.decrypt(row['zip_code']).decode('utf-8') if row['zip_code'] else row['zip_code']),
                str(encrypt.decrypt(row['city']).decode('utf-8') if row['city'] else row['city']),
                str(encrypt.decrypt(row['email_address']).decode('utf-8') if row['email_address'] else row['email_address']),
                str(encrypt.decrypt(row['mobile_phone']).decode('utf-8') if row['mobile_phone'] else row['mobile_phone']),
                str(encrypt.decrypt(row['driving_license_number']).decode('utf-8') if row['driving_license_number'] else row['driving_license_number']),
            ]
            # Score: count of fields containing the search key (higher is better)
            score = sum(search_key_lower in str(field).lower() for field in fields_to_search)
            if score > best_score:
                best_score = score
                best_row = row

        if best_row and best_score > 0:
            traveller = Traveller(
                first_name=encrypt.decrypt(best_row['first_name']).decode('utf-8') if best_row['first_name'] else "",
                last_name=encrypt.decrypt(best_row['last_name']).decode('utf-8') if best_row['last_name'] else "",
                birthday=datetime.strptime(str(encrypt.decrypt(row['birthday']).decode('utf-8')), "%Y-%m-%d").date()if best_row['birthday'] else None,
                gender=encrypt.decrypt(best_row['gender']).decode('utf-8') if best_row['gender'] else "",
                street_name=encrypt.decrypt(best_row['street_name']).decode('utf-8') if best_row['street_name'] else "",
                house_number=encrypt.decrypt(best_row['house_number']).decode('utf-8') if best_row['house_number'] else "",
                zip_code=encrypt.decrypt(best_row['zip_code']).decode('utf-8') if best_row['zip_code'] else "",
                city=encrypt.decrypt(best_row['city']).decode('utf-8') if best_row['city'] else "",
                email_address=encrypt.decrypt(best_row['email_address']).decode('utf-8') if best_row['email_address'] else "",
                mobile_phone=encrypt.decrypt(best_row['mobile_phone']).decode('utf-8') if best_row['mobile_phone'] else "",
                driving_license_number=encrypt.decrypt(best_row['driving_license_number']).decode('utf-8') if best_row['driving_license_number'] else "",
                registration_date= datetime.strptime(best_row['registration_date'], "%Y-%m-%d").date() if best_row['registration_date'] else None,
            )
            return traveller
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
            Utility.log_activity(user.username, "Update scooter to DB", additional_info=f"Update scooter {scooter.serial_number}", suspicious_count = 0)
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
            Utility.log_activity(user.username, "Update scooter to DB", additional_info=f"Update scooter {scooter.serial_number} to DB succesful", suspicious_count = 0)
        except sqlite3.Error as e:
            print("Error updating scooter in the database:", e)
            Utility.log_activity(user.username, "Update scooter to DB", additional_info=f"Update scooter to DB failed: {e}", suspicious_count = 3)
    
    @staticmethod
    def update_account(user: User, user_to_update):
        user_to_update_old = copy.deepcopy(user_to_update) # if you don't use copy, it will change this variable as it only references the old one
        user_to_update = Validate.validate_updateuser(user, user_to_update)
        try:
            encrypt = Utility.load_key()

            conn = sqlite3.connect('users.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT rowid, username FROM users")
            rows = c.fetchall()
            target_rowid = None
            for row in rows:
                decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
                if decrypted_username == user_to_update_old.username:
                    target_rowid = row['rowid']
                    break

            enc_username = encrypt.encrypt(user_to_update.username.encode('utf-8'))
            enc_first_name = encrypt.encrypt(user_to_update.first_name.encode('utf-8'))
            enc_last_name = encrypt.encrypt(user_to_update.last_name.encode('utf-8'))

            if target_rowid is not None:
                c.execute('''
                    UPDATE users
                    SET role = ?, username = ?, password = ?, first_name = ?, last_name = ?
                    WHERE rowid = ?
                ''', (
                    user_to_update.role,
                    enc_username,
                    user_to_update.password,
                    enc_first_name,
                    enc_last_name,
                    target_rowid
                ))
                conn.commit()
                conn.close()
                print("User updated successfully.")
                Utility.log_activity(user.username, "Update user in DB", additional_info=f"User: {user_to_update.username} updated in DB", suspicious_count=0)
            else:
                conn.close()
                print(f"User '{user_to_update.username}' not found.")
                Utility.log_activity(user.username, "Update user in DB", additional_info=f"Update user failed: {user_to_update.username} not found", suspicious_count=3)
        except sqlite3.Error as e:
            print("Error updating user in the database. Please check the input values.")
            print(f"SQLite error: {e}")
            Utility.log_activity(user.username, "Update user in DB", additional_info=f"Update user failed: {e}", suspicious_count=3)
            return
        
    @staticmethod
    def update_backup_code(super_admin: User, target_user: User, restore_code: str):
        try:
            encrypt = Utility.load_key()
            conn = sqlite3.connect('users.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute("SELECT rowid, username FROM users")
            rows = c.fetchall()
            target_rowid = None

            for row in rows:
                decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
                if decrypted_username == target_user.username:
                    target_rowid = row['rowid']
                    break

            if target_rowid is not None:
                c.execute('''
                    UPDATE users
                    SET restore_code = ?
                    WHERE rowid = ?
                ''', (
                    restore_code,
                    target_rowid
                ))
                conn.commit()
                conn.close()
                print("Restore code updated successfully.")
                Utility.log_activity(super_admin.username, "Assigned restore code", additional_info=f"Assigned restore code to {target_user.username}", suspicious_count=0)
            else:
                conn.close()
                print(f"User '{target_user.username}' not found.")
                Utility.log_activity(super_admin.username, "Assign restore code failed", additional_info=f"User not found: {target_user.username}", suspicious_count=3)

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            Utility.log_activity(super_admin.username, "Assign restore code failed", additional_info=str(e), suspicious_count=3)

    

    @staticmethod
    def update_traveller(user: User, traveller: Traveller): #traveller here is decrypted and accurate
        try:
            traveller_old = copy.deepcopy(traveller) #should not be re-encrypted for comparison with database
            traveller = Validate.Validate_addtraveller(user, traveller) #generates a new not-yet-encrypted traveller
            encrypt = Utility.load_key()
            
            conn = sqlite3.connect('travellers.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT rowid, first_name, last_name, birthday, zip_code, email_address FROM travellers")
            rows = c.fetchall()
            target_rowid = None

            print(f"{traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.email_address}, {traveller_old.zip_code}")

            for row in rows: # for each row, decrypt field and find match with traveller_old
                decrypted_first_name = encrypt.decrypt(row['first_name']).decode('utf-8')
                decrypted_last_name = encrypt.decrypt(row['last_name']).decode('utf-8')
                decrypted_birthday = datetime.strptime(str(encrypt.decrypt(row['birthday']).decode('utf-8')), "%Y-%m-%d").date()
                decrypted_zip_code = encrypt.decrypt(row['zip_code']).decode('utf-8')
                decrypted_email_address = encrypt.decrypt(row['email_address']).decode('utf-8')

                if (    decrypted_first_name == traveller_old.first_name #traveller should be decrypted here already
                    and decrypted_last_name == traveller_old.last_name 
                    and decrypted_birthday == traveller_old.birthday
                    and decrypted_zip_code == traveller_old.zip_code
                    and decrypted_email_address == traveller_old.email_address
                    ):
                    target_rowid = row['rowid']
                    break
            if target_rowid is not None:
                
                enc_first_name = encrypt.encrypt(traveller.first_name.encode('utf-8'))
                enc_last_name = encrypt.encrypt(traveller.last_name.encode('utf-8'))
                enc_birthday = encrypt.encrypt(traveller.birthday.isoformat().encode('utf-8'))
                enc_gender = encrypt.encrypt(traveller.gender.encode('utf-8'))
                enc_street_name = encrypt.encrypt(traveller.street_name.encode('utf-8'))
                enc_house_number = encrypt.encrypt(traveller.house_number.encode('utf-8'))
                enc_zip_code = encrypt.encrypt(traveller.zip_code.encode('utf-8'))
                enc_city = encrypt.encrypt(traveller.city.encode('utf-8'))
                enc_email_address = encrypt.encrypt(traveller.email_address.encode('utf-8'))
                enc_mobile_phone = encrypt.encrypt(traveller.mobile_phone.encode('utf-8'))
                enc_driving_license_number = encrypt.encrypt(traveller.driving_license_number.encode('utf-8'))

                conn = sqlite3.connect('travellers.db')
                c = conn.cursor()
                c.execute('''
                    UPDATE travellers SET
                        first_name = ?,
                        last_name = ?,
                        birthday = ?,
                        gender = ?,
                        street_name = ?,
                        house_number = ?,
                        zip_code = ?,
                        city = ?,
                        email_address = ?,
                        mobile_phone = ?,
                        driving_license_number = ?
                    WHERE rowid = ?
                ''', (
                    enc_first_name,
                    enc_last_name,
                    enc_birthday,
                    enc_gender,
                    enc_street_name,
                    enc_house_number,
                    enc_zip_code,
                    enc_city,
                    enc_email_address,
                    enc_mobile_phone,
                    enc_driving_license_number,
                    target_rowid      
                ))
                conn.commit()
                conn.close()
                print(f"traveller attributes updated successfully to {traveller.first_name} {traveller.last_name}")
                Utility.log_activity(user.username, "Updated original traveller {traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code to DB succesful", 
                                    additional_info=f"Updated original traveller {traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code} to DB succesful", suspicious_count = 0)
            else:
                conn.close()
                print(f"traveller '{traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code}' not found.")
                Utility.log_activity(user.username, f"traveller '{traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code}' not found.", suspicious_count=0)

        except sqlite3.Error as e:
            print(f"Error updating traveller {traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code} in the database:", e)
            Utility.log_activity(user.username, f"Update original traveller {traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code} to DB failed", additional_info=f"Update original traveller {traveller_old.first_name} {traveller_old.last_name}, {traveller_old.birthday}, {traveller_old.zip_code} to DB failed: {e}", suspicious_count = 0)


    @staticmethod
    def create_backup(user: User):
        try:
            db_files = ['users.db', 'scooters.db', 'travellers.db']
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
        db_files = ['users.db', 'scooters.db', 'travellers.db']

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
    def generate_backup_code(backup_filename: str, user: User) -> str:
        try:
            backup_path = os.path.join("backups", backup_filename)
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file '{backup_path}' does not exist.")

            # Ensure it starts with "backup_" and ends with ".zip"
            if not (backup_filename.startswith("backup_") and backup_filename.endswith(".zip")):
                raise ValueError("Invalid backup filename format.")
            
            # Strip prefix and suffix
            timestamp_str = backup_filename.replace("backup_", "").replace(".zip", "")

            # Ensure timestamp format is valid
            datetime_obj = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            
            # Format readable restore code
            restore_code = f"RESTORE-{datetime_obj.strftime('%Y%m%d-%H%M%S')}"
            
            # Optional logging
            Utility.log_activity(
                user.username,
                "Generated restore code",
                additional_info=f"Generated code {restore_code} for backup {backup_filename}",
                suspicious_count=0
            )

            return restore_code
        except Exception as e:
            print(f"Failed to generate restore code: {e}")
            Utility.log_activity(
                user.username,
                "Restore code generation failed",
                additional_info=str(e),
                suspicious_count=3
            )
            return None
        

    @staticmethod
    def revoke_backup_code(invoking_user: User, target_user: User):
        try:
            encrypt = Utility.load_key()
            conn = sqlite3.connect('users.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute("SELECT rowid, username FROM users")
            rows = c.fetchall()
            target_rowid = None

            for row in rows:
                decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
                if decrypted_username == target_user.username:
                    target_rowid = row['rowid']
                    break

            if target_rowid is not None:
                c.execute("UPDATE users SET restore_code = NULL WHERE rowid = ?", (target_rowid,))
                conn.commit()
                conn.close()

                if invoking_user.role == "Super Administrator":
                    print(f"Restore code revoked for '{target_user.username}'.")
                    Utility.log_activity(
                        invoking_user.username,
                        "Revoked restore code",
                        additional_info=f"Restore code revoked from {target_user.username}",
                        suspicious_count=0
                    )
                elif invoking_user.role == "System Administrator":
                    # Used internally after a restore
                    print("Restore code cleared after successful restoration.")
                    Utility.log_activity(
                        invoking_user.username,
                        "System restore",
                        additional_info=f"Restore code automatically cleared after restoring from backup.",
                        suspicious_count=0
                    )
                else:
                    print("Restore code revoked.")
            else:
                conn.close()
                print(f"User '{target_user.username}' not found.")
                Utility.log_activity(
                    invoking_user.username,
                    "Revoke restore code failed",
                    additional_info=f"User not found: {target_user.username}",
                    suspicious_count=3
                )

        except sqlite3.Error as e:
            print(f"SQLite error while revoking restore code: {e}")
            Utility.log_activity(
                invoking_user.username,
                "Revoke restore code failed",
                additional_info=str(e),
                suspicious_count=3
            )



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
    def delete_traveller(user: User, traveller: Traveller):
        encrypt = Utility.load_key()

        conn = sqlite3.connect('travellers.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rowid, first_name, last_name, birthday, zip_code FROM travellers")
        rows = c.fetchall()
        for row in rows:
            print(row.keys())

        target_rowid = None
        for row in rows:
            decrypted_first_name = encrypt.decrypt(row['first_name']).decode('utf-8')
            decrypted_last_name = encrypt.decrypt(row['last_name']).decode('utf-8')
            decrypted_birthday = encrypt.decrypt(row['birthday']).decode('utf-8')
            decrypted_zip_code = encrypt.decrypt(row['zip_code']).decode('utf-8')
            if decrypted_first_name == traveller.first_name and decrypted_last_name == traveller.last_name and decrypted_birthday == traveller.birthday and decrypted_zip_code == traveller.zip_code: 
                target_rowid = row['rowid']
                break

        if target_rowid is not None:
            c.execute("DELETE FROM travellers WHERE rowid = ?", (target_rowid,))
            conn.commit()
            conn.close()
            print(f"traveller '{traveller.first_name} {traveller.last_name}, {traveller.birthday}, {traveller.zip_code}' deleted successfully.")
            Utility.log_activity(user.username, "Delete traveller from DB", additional_info=f"Deleted traveller: {traveller.first_name} {traveller.last_name}, {traveller.birthday}, {traveller.zip_code} from DB", suspicious_count = 0)
        else:
            print(f"traveller '{traveller.first_name} {traveller.last_name}, {traveller.birthday}, {traveller.zip_code}' not found.")
            Utility.log_activity(user.username, "Delete traveller from DB", additional_info=f"Failed to delete traveller: {traveller.first_name} {traveller.last_name}, {traveller.birthday}, {traveller.zip_code} from DB", suspicious_count = 3)

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

    @staticmethod
    def print_travelerinfo(traveller: Traveller):
        print("=== User Information ===")
        print(f"First Name: {traveller.first_name}")
        print(f"Last Name: {traveller.last_name}")
        print(f"Birth Date: {traveller.birthday}")
        print(f"Gender: {traveller.gender}")
        print(f"Street Name: {traveller.street_name}")
        print(f"House Number: {traveller.house_number}")
        print(f"Zipcode: {traveller.zip_code}")
        print(f"City: {traveller.city}")
        print(f"Email Address: {traveller.email_address}")
        print(f"Mobile Phone Number: {traveller.mobile_phone}")
        print(f"Driving License Number: {traveller.driving_license_number}")
        print(f"Registration Date: {traveller.registration_date.isoformat()}")


    @staticmethod
    def get_backup_filename_from_restore_code(restore_code: str) -> str:
        try:
            if not restore_code.startswith("RESTORE-"):
                return None
            timestamp = restore_code.replace("RESTORE-", "").replace("-", "_")
            backup_filename = f"backup_{timestamp}.zip"
            backup_path = os.path.join("backups", backup_filename)
            return backup_filename if os.path.exists(backup_path) else None
        except:
            return None


    @staticmethod
    def update_temp_password(admin_user: User, target_username: str, temp_password: str | None):
        """
        Assign or clear a temporary password.
        If temp_password is None, the field is cleared in the database.
        """
        try:
            encrypt = Utility.load_key()
            conn = sqlite3.connect('users.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Fetch all users and find the matching user by decrypted username
            c.execute("SELECT rowid, username, role FROM users")
            rows = c.fetchall()

            target_rowid = None
            for row in rows:
                decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
                if decrypted_username == target_username and row['role'] in ["Service Engineer", "System Administrator"]:

                    target_rowid = row['rowid']
                    break

            if target_rowid is not None:
                if temp_password is None:
                    c.execute("""
                        UPDATE users
                        SET temp_password = NULL
                        WHERE rowid = ?
                    """, (target_rowid,))
                    message = f"Temporary password for '{target_username}' has been cleared."
                else:
                    encrypted_temp_pass = encrypt.encrypt(temp_password.encode('utf-8'))
                    c.execute("""
                        UPDATE users
                        SET temp_password = ?
                        WHERE rowid = ?
                    """, (encrypted_temp_pass, target_rowid))
                    message = f"Temporary password set for '{target_username}'."

                conn.commit()
                conn.close()
                print(message)
                Utility.log_activity(
                    admin_user.username,
                    "Updated temp password",
                    additional_info=message,
                    suspicious_count=0
                )
            else:
                conn.close()
                print(f"User '{target_username}' not found.")
                Utility.log_activity(
                    admin_user.username,
                    "Assign temp password failed",
                    additional_info=f"User not found or not a Service Engineer/System Administrator: {target_username}",
                    suspicious_count=3
                )
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            Utility.log_activity(
                admin_user.username,
                "Assign temp password failed",
                additional_info=str(e),
                suspicious_count=3
            )



    @staticmethod
    def generate_temp_password(length=12):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def lock_account(user: User):
        try:
            encrypt = Utility.load_key()
            conn = sqlite3.connect('users.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute("SELECT rowid, username FROM users")
            rows = c.fetchall()
            target_rowid = None
            for row in rows:
                decrypted_username = encrypt.decrypt(row['username']).decode('utf-8')
                if decrypted_username == user.username:
                    target_rowid = row['rowid']
                    break

            if target_rowid is not None:
                c.execute("UPDATE users SET locked = 1 WHERE rowid = ?", (target_rowid,))
                conn.commit()
                conn.close()
                print(f"Account for '{user.username}' has been locked due to multiple failed login attempts.")
                Utility.log_activity(
                    user.username,
                    "Account locked",
                    additional_info=f"Account locked after multiple failed login attempts for user: {user.username}",
                    suspicious_count=3
                )
            else:
                conn.close()
                print(f"User '{user.username}' not found for locking.")
                Utility.log_activity(
                    user.username,
                    "Account lock failed",
                    additional_info="User not found for locking.",
                    suspicious_count=3
                )
        except sqlite3.Error as e:
            print(f"SQLite error while locking account: {e}")
            Utility.log_activity(
                user.username,
                "Account lock failed",
                additional_info=str(e),
                suspicious_count=3
            )