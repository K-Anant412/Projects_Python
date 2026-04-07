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
@employee_route.route("/add_employee")# add new employee__
class create_emp(Resource):
    @employee_route.expect(employee_model)
    def post(self):
        data = request.get_json()
        return create_employee(data)
@employee_route.route("/show_employee")# show all employee's__
class show_employee(Resource):
    @employee_route.doc(params={
        'page': {'description': 'Page number', 'type': 'int', 'default': 1},
        'per_page': {'description': 'Employees per page', 'type': 'int', 'default': 4}
    })
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)
        return get_all_employees(page=page, per_page=per_page) 
@employee_route.route("/emp_by_id/<int:id>")# show employee by ID__
@employee_route.param("id")
class show_employee_by_id(Resource):
    def get(self, id) :
        return get_emp_by_id(id)
    
parser = reqparse.RequestParser()
parser.add_argument("min_salary", type=float, required=True)
parser.add_argument("max_salary", type=float, required=True)
@employee_route.route("/filter_by_salary")# show employee's, filter by salary__ 
class filter_salary(Resource):
        @employee_route.expect(parser)
        def get(self):
            args = parser.parse_args()
            return get_emp_by_salary(
                args["min_salary"],
                args["max_salary"]
            )
@employee_route.route("/update_employee/<int:id>")# update existing employee by ID__
class update_employee(Resource):
    @employee_route.param("id", "employee id", _in="path", required=True)
    @employee_route.doc(params={
        "role":{
            "in": "header",
            "description": "user role should be superadmin",
            "required": True
        }
    })
    @employee_route.expect(employee_model)
    def put(self, id):
        role = request.headers.get("role")
        data = request.get_json()
        return update_emp_by_id(id, data, role)
    
@employee_route.route("/delete_employee/<int:id>")# remove employee by ID__
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