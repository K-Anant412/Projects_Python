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

def find_by_id(data):
    try:
        emp = Employee.query.filter_by(id=data["id"]).first()
        if not emp:
            return error_response("employee not exist", 400)
        e = Employee.query.get(data["id"])
        return success_response(str(e))
    except Exception as e:
        return error_response(str(e))

def update_employee(data):
    try:
        emp = Employee.query.get(data["id"])
        if not emp:
            return error_response("employee not exist", 400)
        if "name" in data:
            emp.name = data["name"]        
        if "email" in data:
            emp.email = data["email"]        
        if "salary" in data:
            emp.salary = data["salary"]        
        if "department" in data:
            emp.department = data["department"]  
        db.session.commit()      
        
    except Exception as e:
        return error_response(str(e))
    
def delete_employee(data):
    try:
        emp = Employee.query.filter_by(id=data["id"]).first()
        if not emp:
            return error_response("employee not exist", 400)
        db.session.delete(emp)
        db.session.commit()
        return success_response("employee removed")
    except Exception as e:
        return error_response(str(e))
    