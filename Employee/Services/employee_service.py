from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Validation import employee_validation
from Modules.employee_module import Employee
from Modules.department_module import Department

def create_employee(data):
    
    try:
        error = employee_validation(data)
        
        if error:
            return error_response("enter required information")
        
        dp = Department.query.filter_by(name=data["department"]).first()
        if not dp:
            return error_response("department not found", 400)
        
        employee = Employee(
                            name=data["name"], 
                            email=data["email"], 
                            salary=data["salary"], 
                            department=dp.id
                            )
        db.session.add(employee)
        db.session.commit()
        
        return success_response("employee added")
    
    except Exception as e :
        return error_response(str(e))