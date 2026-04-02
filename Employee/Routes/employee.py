from flask import request
from flask_restx import Namespace, Resource, fields
from Services.employee_service import (create_employee, delete_employee, find_by_id, update_employee)

employee_routes = Namespace("employee", description="creating new employee")
employee_model = employee_routes.model("Employee", {
                                               "name": fields.String(required=True, description="employee name"),
                                               "email": fields.String(required=True, description="employee email"),
                                               "salary": fields.String(required=True, description="employee salary"),
                                               "department": fields.String(required=True, description="employee department")
                                               }
                                 )
@employee_routes.route("/add_employee")
class create_emp(Resource):
    @employee_routes.expect(employee_model)
    def post(self):
        data = request.get_json()
        return create_employee(data)
    
find_emp_route = Namespace("By ID", description="find employee by id")
employee_id = find_emp_route.model("Employee_ID", {"id": fields.String(required=True, description="enter employee id")})
@find_emp_route.route("/find_employee")
class show_by_id(Resource):
    @find_emp_route.doc(params = {"id":"enter employee id"})
    def get(self):
        emp_id = request.args.get("id")
        return find_by_id({"id":emp_id})

update_emp_route = Namespace("Update", description="update existing employee information")
employee_id = update_emp_route.model("Employee_ID", {"id": fields.String(required=True, description="enter employee id")})
@update_emp_route.route("/update_employee")
class update_employee(Resource):
    @update_emp_route.expect(employee_model)
    def post(self):
        emp_id = request.args.get("id")
        return update_employee(emp_id)

delete_emp_route = Namespace("remove employee", description="remove existing employee")
employee_id = delete_emp_route.model("Employee_ID", {"id": fields.String(required=True, description="enter employee id")})
@delete_emp_route.route("/delete_employee")
class delete_emp(Resource):
    @delete_emp_route.expect(employee_id)
    def post(self):
        data = request.get_json()
        return delete_employee(data)