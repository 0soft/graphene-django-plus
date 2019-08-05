try:
    from graphql_jwt.exceptions import PermissionDenied
except ImportError:
    class PermissionDenied(Exception):
        default_message = "You do not have permission to perform this action"
