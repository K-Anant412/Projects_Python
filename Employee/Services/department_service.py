from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Validation import department_validation
from Modules.department_module import Department

def create_department(data):
    try:
        error = department_validation(data)
        
        if error:
            return error_response("enter department name")
        
        department = Department(name=data["name"])
        
        db.session.add(department)
        db.session.commit()
        
        return success_response("department was created")
    except Exception as e:
        return error_response(str(e))