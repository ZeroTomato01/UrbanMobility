from InitDB import InitDB
from Menu import Menu
from permissions import Permissions
from SeedDB import SeedDB


def main():
    user = Menu.login()
    while True:
        if Permissions.has_permission(user, "super_menu"):
            Menu.super_admin_menu(user)
        elif Permissions.has_permission(user, "system_menu"):
            Menu.system_admin_menu(user)
        elif Permissions.has_permission(user, "service_menu"):
            Menu.service_engineer_menu(user)

if __name__ == "__main__":
    main()