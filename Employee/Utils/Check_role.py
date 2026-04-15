from Utils.Response import error_response
from functools import wraps
from flask import session

def check_role(allowed_role):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = session.get("role")
            if not role:
                return error_response("unauthrized user", 500)
            if role not in allowed_role:
                return error_response("access not allowed")
            return func(*args, **kwargs)
        return wrapper
    return decor