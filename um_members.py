from Utils import Utility
from InitDB import InitDB
from Menu import login, super_admin_menu, system_admin_menu, service_engineer_menu


def main():
    while True:
        role = login()
        if role == "Super Administrator":
            super_admin_menu()
        elif role == "System Administrator":
            system_admin_menu()
        elif role == "Service Engineer":
            service_engineer_menu()
        else:
            break

if __name__ == "__main__":
    main()