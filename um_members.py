from Utils import Utility
from InitDB import InitDB
from Menu import Menu


def main():
    user = Menu.login()
    while True:
        if user.role == "Super Administrator":
            Menu.super_admin_menu()
        elif user.role == "System Administrator":
            Menu.system_admin_menu()
        elif user.role == "Service Engineer":
            Menu.service_engineer_menu()

if __name__ == "__main__":
    main()