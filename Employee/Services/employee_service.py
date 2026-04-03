from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Validation import employee_validation
from Modules.employee_module import Employee
from Modules.department_module import Department

#add new employee
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

def get_all_employees():
    employee = Employee.query.all()
    result = []
    for emp in employee:
        result.append({
            "Id":emp.id,
            "name":emp.name,
            "email":emp.email,
            "salary":emp.salary,
            "department":emp.department.name if emp.department else None
        })
    return success_response("Employee fecthed", result)

def get_emp_by_id(id):
    emp = db.session.get(Employee, id)
    if not emp:
        return error_response("Employee not found")
    result = {
        "name":emp.name,
        "email":emp.email,
        "salary":emp.salary
    }
    return success_response("Employee found", result)

def update_emp_by_id(id, data):
    try:
        emp = db.session.get(Employee, id)
        if not emp:
            return error_response("Employee not found")
        if "department" in data:
            dept = Department.query.filter_by(name=data["department"]).first()
            if not dept:
                return error_response("Department not found")
            emp.id = dept.id
        if "name" in data:
            emp.name = data["name"]
        if "email" in data:
            emp.email = data["email"]
        if "salary" in data:
            emp.salary = data["salary"]
        db.session.commit()
        result = {
            "name": emp.name,
            "email": emp.email,
            "salary": emp.salary,
            "department": emp.department.name if emp.department else None
        }
        return success_response("employee updated", result)
        
    except Exception as e:
        return error_response(str(e))
    
    
def delete_employee(id):
    try:
        emp = db.session.get(Employee, id)
        if not emp:
            return error_response("Employee not found")
        db.session.delete(emp)
        db.session.commit()
        return success_response("Employee was deleted")
    except Exception as e:
        return error_response(str(e))
    
    
    
    
    
    
    
    
    
    
    
# #find employee by ID
# def find_by_id(data):
#     try:
#         emp = Employee.query.filter_by(id=data["id"]).first()
#         if not emp:
#             return error_response("employee not exist", 400)
#         e = Employee.query.get(data["id"])
#         return success_response(str(e))
#     except Exception as e:
#         return error_response(str(e))

# #update employee information
# def update_employee(data):
#     try:
#         emp = Employee.query.get(data["id"])
#         if not emp:
#             return error_response("employee not exist", 400)
#         if "name" in data:
#             emp.name = data["name"]        
#         if "email" in data:
#             emp.email = data["email"]        
#         if "salary" in data:
#             emp.salary = data["salary"]        
#         if "department" in data:
#             emp.department = data["department"]  
#         db.session.commit()      
        
#     except Exception as e:
#         return error_response(str(e))

# #remove an employee information using ID
# def delete_employee(data):
#     try:
#         emp = Employee.query.filter_by(id=data["id"]).first()
#         if not emp:
#             return error_response("employee not exist", 400)
#         db.session.delete(emp)
#         db.session.commit()
#         return success_response("employee removed")
#     except Exception as e:
#         return error_response(str(e))
    
    
# def  get_emp_by_id(id):
#     try:
        
#        empolee= Employee.query.get(id)
       
#        if not empolee:
#            return error_response("empolyee not found")
       
#        result={
#            "id":empolee.id,
#            "name": empolee.name,
#            "email":empolee.email,
#            "salary":empolee.salary,
#            "department":empolee.deparment.name if empolee.department else "not fount"
#        }
       
#        return success_response(result)
        
#     except Exception as e :
#         print(str(e))    
    
    