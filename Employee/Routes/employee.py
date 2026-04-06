from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from Services.employee_service import (create_employee, get_all_employees, get_emp_by_id, update_emp_by_id,delete_employee, get_emp_by_salary)

employee_route = Namespace("employees", description="show all employee's")
employee_model = employee_route.model("Employee",{
                                               "name": fields.String(required=True, description="employee name"),
                                               "email": fields.String(required=True, description="employee email"),
                                               "salary": fields.String(required=True, description="employee salary"),
                                               "department": fields.String(required=True, description="employee department")
                                               })
@employee_route.route("/add_employee")
class create_emp(Resource):
    @employee_route.expect(employee_model)
    def post(self):
        data = request.get_json()
        return create_employee(data)
@employee_route.route("/show_employee")
class show_employee(Resource):
    def get(self):
        return get_all_employees() 
@employee_route.route("/emp_by_id/<int:id>")
@employee_route.param("id")
class show_employee_by_id(Resource):
    def get(self, id) :
        return get_emp_by_id(id)
    
parser = reqparse.RequestParser()
parser.add_argument("min_salary", type=float, required=True)
parser.add_argument("max_salary", type=float, required=True)
@employee_route.route("/filter_by_salary")
class filter_salary(Resource):
        @employee_route.expect(parser)
        def get(self):
            args = parser.parse_args()
            return get_emp_by_salary(
                args["min_salary"],
                args["max_salary"]
            )
@employee_route.route("/update_employee/<int:id>")
@employee_route.param("id")
class update_employee(Resource):
    @employee_route.expect(employee_model)
    def put(self, id):
        data = request.get_json()
        return update_emp_by_id(id, data)
@employee_route.route("/delete_employee/<int:id>")
class delete_emp(Resource):
    @employee_route.param("id", "Employee ID", _in="path", required=True)
    @employee_route.doc(params={
        "role": {
            "in": "header",
            "description": "user role admin or superadmin",
            "required": True
        }
    })                        
    def delete(self, id):
        print("API running")
        role = request.headers.get("Role")
        return delete_employee(id, role)