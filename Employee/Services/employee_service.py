from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Check_role import check_superadmin
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

def get_all_employees(page=1, per_page=4):
    pag_obj = Employee.query.paginate(page=page, per_page=per_page, error_out=False)
    employee = Employee.query.all()
    employee = pag_obj.items
    result = []
    for emp in employee:
        result.append({
            "Id":emp.id,
            "name":emp.name,
            "email":emp.email,
            "salary":emp.salary,
            "department":emp.department_id if emp.department_id else None
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

def get_emp_by_salary(min_salary, max_salary):
    try:
        data = []
        employees = Employee.query.filter(
            Employee.salary >= min_salary,
            Employee.salary <= max_salary
        ).all()
        for emp in employees:
            data.append({
                "name": emp.name,
                "salary": emp.salary
            })
            
        return success_response("Employees", data)
    except Exception as e:
        return error_response(str(e))

def update_emp_by_id(id, data, role):
    try:
        error = check_superadmin(role)
        if error:
            return error
        
        emp = db.session.get(Employee, id)
        if not emp:
            return error_response("Employee not found")
        
        if "department" in data:
            dept = Department.query.filter_by(name=data["department"]).first()
            
            if not dept:
                return error_response("Department not found")
            emp.department_id = dept.id
            
        if "name" in data:
            emp.name = data["name"]
        if "email" in data:
            emp.email = data["email"]
        if "salary" in data:
            emp.salary = data["salary"]
        db.session.commit()
        
        dept_name = None
        if emp.department_id:
            dept_obj = db.session.get(Department, emp.department_id)
            if dept_obj:
                dept_name = dept_obj.name

        result = {
            "name": emp.name,
            "email": emp.email,
            "salary": emp.salary,
            "department": dept_name # Use the manually fetched name
        }
        return success_response("employee updated", result)
        
    except Exception as e:
        return error_response(str(e))
    
    
def delete_employee(id, role):
    try:
        error = check_superadmin(role)
        if error:
            return error
        emp = db.session.get(Employee, id)
        if not emp:
            return error_response("Employee not found")
        db.session.delete(emp)
        db.session.commit()
        return success_response("Employee was deleted")
    except Exception as e:
        return error_response(str(e))