from Models import User

class Permissions:
    @staticmethod
    def has_permission(user: User, action: str) -> bool:

        role_permissions = {
            "Super Administrator": {
                # Add permitted actions here

            },
            "System Administrator": {
                # Add permitted actions here

            },
            "Service Engineer": {
                # Add permitted actions here
            }
        }

        allowed_actions = role_permissions.get(user.role, set())
        return action in allowed_actions
