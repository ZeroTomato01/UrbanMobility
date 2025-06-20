from Models import User

class Permissions:
    @staticmethod
    def has_permission(user: User, action: str) -> bool:

        role_permissions = {
            "Super Administrator": {
                "generate_restore_code",
                "revoke_backup_code",
                "assign_temp_password",
                "restore_backup",
                "super_menu",
                "super_del_account",
                # Add permitted actions here
            },
            "System Administrator": {
                "system_menu",
                "system_del_account",
                "restore_backup",
                "assign_temp_password",
                "lockable",
                # Add permitted actions here

            },
            "Service Engineer": {
                "service_menu",
                "lockable",
                # Add permitted actions here
            }
        }

        allowed_actions = role_permissions.get(user.role, set())
        return action in allowed_actions
