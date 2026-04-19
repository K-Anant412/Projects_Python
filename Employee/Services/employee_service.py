from DataBase.database import db
import pandas as pd
from Utils.Response import error_response, success_response
# from Utils.Check_role import check_superadmin
from Utils.Validation import employee_validation
from Modules.employee_module import Employee
from Modules.department_module import Department
from reportlab.platypus import SimpleDocTemplate, Table
from io import BytesIO
from flask import send_file, request

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
                            city=data["city"],
                            email=data["email"], 
                            salary=data["salary"], 
                            department_id=dp.id
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
            "city":emp.city,
            "email":emp.email,
            "salary":emp.salary,
            "department":emp.department_id if emp.department_id else None
        })
    return success_response("Employee fecthed", result)

def sort_emp(page=1, per_page=5):
    try:
        page_obj = Employee.query.order_by(Employee.salary).paginate(
                                            page=page, 
                                            per_page=per_page, 
                                            error_out=False
                                            )
        employee = page_obj.items
        data = []
        for emp in employee:
            data.append({
                "Id":emp.id,
                "name":emp.name,
                "salary":emp.salary,
                "department":emp.department_id if emp.department_id else None
            })
        return success_response("Employee fetched", data)
    except Exception as e:
        return error_response(str(e))
    
    
def search_emp(**kwargs):
    emp = db.select(Employee)
    
    if kwargs.get("id"):
        emp = emp.filter(Employee.id == kwargs["id"])
    if kwargs.get("name"):
        emp = emp.filter(Employee.name.like(f"%{kwargs['name']}%"))
    if kwargs.get("city"):
        emp = emp.filter(Employee.city == kwargs["city"])
    if kwargs.get("department"):
        emp = emp.join(Department).filter(Department.name == kwargs['department'])
    
    result = db.session.execute(emp).scalars().all()
    
    if not result:
        return error_response("No employees found matching criteria", 404)
    
    output = []
    for item in result:
        output.append({
            "ID": item.id,
            "Name": item.name,
            "City": item.city,
            "Department": item.department.name if item.department else "No Department"
        })
        
    return success_response(output)
    
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

def update_emp_by_id(id, data):
    try:
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
            try:
                emp.salary = float(data["salary"])
            except:
                return error_response("Invalid salary format")
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
        print(e)
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
    
def emp_pdf():
    try:
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(buffer)
        
        employees = Employee.query.all()
        
        data = [["ID", "Name", "City", "Contact", "Salary", "Department"]]
        
        for emp in employees:
            data.append([
                emp.id,
                emp.name,
                emp.city,
                emp.email,
                emp.salary,
                emp.department.name if emp.department else "No Department"
            ])
            
        table = Table(data)
        doc.build([table])
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name="employees.pdf", mimetype='application/pdf')
    except Exception as e:
        return error_response(str(e))
    
def upload_emp(f):
    try:
        if not f:
            return error_response("File not found")
        
        df = pd.read_csv(f)
        
        employees = []
        
        for _, row in df.iterrows():
            emp = Employee(
                name = row["name"],
                email = row["email"],
                city = row["city"],
                department_id = row["department_id"],
                salary = row["salary"]
            )
            employees.append(emp)
            
        db.session.bulk_save_objects(employees)
        db.session.commit()
        
        return success_response("Employee's added")
    except Exception as e:
        return error_response(str(e))