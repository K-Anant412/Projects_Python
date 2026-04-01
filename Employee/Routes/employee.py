from flask import request
from flask_restx import Namespace, Resource, fields
from Services.employee_service import create_employee

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