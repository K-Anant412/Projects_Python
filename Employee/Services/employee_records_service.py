from Utils.Response import error_response, success_response
from Modules.employee_module import Employee
from DataBase.database import db
from datetime import date
from Modules.attendance_module import Attendance

def show_all_employees():

    try:
        data = Employee.query.all()
        employees = []

        for emp in data:
            existing = Attendance.query.filter_by(
                employee_id=emp.id,
                attendance_date=date.today()
            ).first()
            employees.append({
                "ID": emp.id,
                "Name": emp.name,
                "Department": emp.department.name,
                "Attendance Marked": (
                    existing.status if existing
                    else "Not Marked"
                )
            })
        return success_response(employees)
    except Exception as e:
        return error_response(str(e))
    
def employee_month_analysis(id):
    try:
       employee = db.session.get(Employee, id)
       if not employee:
           return error_response("Employee not found")
       result = {
           "id":id,
           "name":employee.name,
           "department":employee.department.name if employee.department else "No department found"
       } 
       return success_response("Employee found",result)
    except Exception as e:
        return error_response(str(e))