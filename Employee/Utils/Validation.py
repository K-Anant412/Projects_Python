def employee_validation(data):
    if not data.get("name"):
        return "enter user name"
    if not data.get("department"):
        return "enter department"
    if not data.get("email"):
        return "enter email"
    if not data.get("salary"):
        return "enter salary"
    return None
    
def department_validation(data):
    if not data.get("name"):
        return "enter department name"
    