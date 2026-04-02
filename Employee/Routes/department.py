from flask import request
from flask_restx import Namespace, Resource, fields
from Services.department_service import create_department

department_routes = Namespace("department", description="creating department")
department_model = department_routes.model("Department",{"name":fields.String(required=True, description="enter department name")})

@department_routes.route("/add_department")
class create_dep(Resource):
    @department_routes.expect(department_model)    
    def post(self):
        data = request.get_json()
        return create_department(data)
    