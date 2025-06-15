import sqlite3

class Menu:
    def login():
        print("=== Urban Mobility Backend System ===")
        username = input("Username: ")
        password = input("Password: ")



        if username == "super_admin" and password == "Admin_123?":
            return "Super Administrator"
        elif username == "sysadmin":
            return "System Administrator"
        elif username == "engineer":
            return "Service Engineer"
        else:
            print("Invalid credentials.")
            return None

    def service_engineer_menu():
        while True:
            print("\n--- Service Engineer Menu ---")
            print("1. Update own password")
            print("2. Update scooter attributes")
            print("3. Search/retrieve scooter info")
            print("0. Logout")
            choice = input("Select an option: ")
            if choice == "0":
                break
            # TODO: Implement each option

    def system_admin_menu():
        while True:
            print("\n--- System Administrator Menu ---")
            print("1. Update own password")
            print("2. Update scooter attributes")
            print("3. Search/retrieve scooter info")
            print("4. List users and roles")
            print("5. Add Service Engineer")
            print("6. Update Service Engineer profile")
            print("7. Delete Service Engineer")
            print("8. Reset Service Engineer password")
            print("9. Update own profile")
            print("10. Delete own account")
            print("11. Backup system")
            print("12. Restore backup (with restore-code)")
            print("13. View logs")
            print("14. Add Traveller")
            print("15. Update Traveller")
            print("16. Delete Traveller")
            print("17. Add Scooter")
            print("18. Delete Scooter")
            print("19. Search/retrieve Traveller info")
            print("0. Logout")
            choice = input("Select an option: ")
            if choice == "0":
                break
            # TODO: Implement each option

    def super_admin_menu():
        while True:
            print("\n--- Super Administrator Menu ---")
            print("1. Update scooter attributes")
            print("2. Search/retrieve scooter info")
            print("3. List users and roles")
            print("4. Add Service Engineer")
            print("5. Update Service Engineer profile")
            print("6. Delete Service Engineer")
            print("7. Reset Service Engineer password")
            print("8. View logs")
            print("9. Add Traveller")
            print("10. Update Traveller")
            print("11. Delete Traveller")
            print("12. Add Scooter")
            print("13. Update Scooter")
            print("14. Delete Scooter")
            print("15. Search/retrieve Traveller info")
            print("16. Add System Administrator")
            print("17. Update System Administrator profile")
            print("18. Delete System Administrator")
            print("19. Reset System Administrator password")
            print("20. Backup system")
            print("21. Restore backup")
            print("22. Generate restore-code")
            print("23. Revoke restore-code")
            print("0. Logout")
            choice = input("Select an option: ")
            if choice == "0":
                break
            # TODO: Implement each option
