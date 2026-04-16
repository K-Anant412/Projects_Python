from flask import request
from Services.employee_records_service import show_all_employees
from flask_restx import Namespace, fields, Resource
from Modules.attendance_module import Attendance
from datetime import date
from DataBase.database import db
from Utils.Response import error_response, success_response

records_route = Namespace("employee_records", description="employee attendance")
records_modle = records_route.model("records", {
    "employee_id": fields.Integer,
    "status": fields.Boolean
})
records_attendance = records_route.model("list",{
    "records": fields.List(fields.Nested(records_modle))
})

@records_route.route("/employees")
class show_employee_list(Resource):
    def get(self):
        return show_all_employees()
    
@records_route.route("/attendance")
class employee_attendance(Resource):
    @records_route.expect(records_attendance)
    def post(self):
        try:
            data = request.get_json()
            records = data.get("records", [])
            
            for record in records:
                emp_id = record.get("employee_id")
                status = record.get("status")
            
                existing = Attendance.query.filter_by(
                            employee_id=emp_id,
                            date=date.today()
                        ).first()
                if existing:
                    continue
                
                attendance = Attendance(
                    employee_id = emp_id,
                    status = status,
                    date = date.today()
                )
    
                db.session.add(attendance)
            db.session.commit()
            
            return success_response('Employee present')
        
        except Exception as e:
            return error_response(str(e))