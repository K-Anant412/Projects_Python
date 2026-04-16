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
            employee_id = emp.id,
            date = date.today()
            ).first()
        
           employees.append({
                "ID":emp.id,
                "Name":emp.name,
                "Attendance marked": "Present" if emp.status else "Absent" 
            })
            
            
        return success_response(employees)
    
    except Exception as e:
        return error_response(str(e))

