from flask import request
from flask_restx import Namespace, Resource, fields
from Services.department_service import (create_department, delete_department, update_department, show_all_department)

department_routes = Namespace("department", description="creating department")
department_model = department_routes.model("Department",{"name":fields.String(required=True, description="enter department name")})

@department_routes.route("/add_department")
class create_dep(Resource):
    @department_routes.expect(department_model)    
    def post(self):
        data = request.get_json()
        return create_department(data)
@department_routes.route("/show_department")
class show_dep(Resource):
    def get(self):
        return show_all_department()
    
@department_routes.route("/update_department/<int:id>")
@department_routes.param("id")
class update_dep(Resource):
    @department_routes.expect(department_model)
    def put(self, id):
        data = request.get_json()
        return update_department(id, data)
@department_routes.route("/delete_department/<int:id>")
@department_routes.param("id")
class remove_dep(Resource):
    def delete(self, id):
        return delete_department(id)