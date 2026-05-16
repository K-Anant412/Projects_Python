from datetime import (
    datetime,
    date
)

from DataBase.database import db

from Modules.employee_module import Employee
from Modules.attendance_module import Attendance

from Utils.Response import (
    success_response,
    error_response
)

def mark_attendance(data):

    try:

        employee_id = data.get(
            "employee_id"
        )

        employee = db.session.get(
            Employee,
            employee_id
        )

        if not employee:
            return error_response(
                "Employee not found"
            )

        existing = Attendance.query.filter_by(
            employee_id=employee_id,
            attendance_date=date.today()
        ).first()

        if existing:
            return error_response(
                "Attendance already marked"
            )

        now = datetime.now()

        if now.hour >= 12:

            status = "Half Day"

        else:

            status = "Present"

        attendance = Attendance(

            employee_id=employee_id,

            attendance_date=date.today(),

            check_in=now,

            status=status
        )

        db.session.add(attendance)

        db.session.commit()

        return success_response(
            "Attendance marked successfully",
            {
                "status": status
            }
        )

    except Exception as e:

        db.session.rollback()

        return error_response(str(e))
    
def month_analysis(id):
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