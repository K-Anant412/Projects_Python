from flask import request
from Services.employee_records_service import show_all_employees, employee_month_analysis
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
                    attendance_date=date.today()
                ).first()
                if existing:
                    continue
                attendance = Attendance(
                    employee_id=emp_id,
                    status=status,
                    attendance_date=date.today()
                )
                db.session.add(attendance)
            db.session.commit()
            return success_response(
                "Attendance marked successfully"
            )
        except Exception as e:
            db.session.rollback()
            return error_response(str(e))


@records_route.route("/month_analysis/<int:id>")
@records_route.param("id")
class employee_analysis(Resource):
    
    def get(self, id):
        return employee_month_analysis(id)