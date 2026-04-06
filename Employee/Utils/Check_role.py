from Utils.Response import error_response

def check_superadmin(role):
    try:
        if role != "superadmin":
            return error_response("only superadmin allow", 403)
        return None
    except Exception as e:
        return error_response(str(e))